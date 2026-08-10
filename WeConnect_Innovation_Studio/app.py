import io
import json
import os
import random
import sqlite3
import sys
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, jsonify, redirect, render_template, request, url_for
from google import genai

# Load environment variables from .env file
load_dotenv()

# Initialize Gemini Client
ai_client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

app = Flask(__name__)
DB_FILE = 'devprep.db'


def get_db_connection():
  conn = sqlite3.connect(DB_FILE)
  conn.row_factory = sqlite3.Row
  return conn


def init_db():
  conn = get_db_connection()
  with open('schema.sql', 'r') as f:
    conn.executescript(f.read())

  cursor = conn.cursor()
  cursor.execute('SELECT COUNT(*) FROM problems')
  if cursor.fetchone()[0] == 0:
    sample_problems = [
        (
            'Remove Duplicates from Sorted Array (LeetCode #26)',
            'Array / Two Pointers',
            'Easy',
            (
                'Given an integer array nums sorted in non-decreasing order,'
                ' remove the duplicates in-place such that each unique element'
                ' appears only once.'
            ),
            'def solution(nums):\n    # Write your solution here\n    pass\n',
            (
                'def solution(nums):\n    if not nums:\n        return 0\n    k ='
                ' 1\n    for i in range(1, len(nums)):\n        if nums[i] !='
                ' nums[i - 1]:\n            nums[k] = nums[i]\n           '
                ' k += 1\n    return nums[:k]\n'
            ),
            json.dumps([
                {'input': 'solution([1, 1, 2])', 'expected': '[1, 2]'},
                {'input': 'solution([0, 0, 1, 1, 2])', 'expected': '[0, 1, 2]'},
            ]),
            'O(N) Time | O(1) Space',
        ),
        (
            'Letter Combinations of a Phone Number (LeetCode #17)',
            'Hash Table / Backtracking',
            'Medium',
            (
                'Given a string containing digits from 2-9 inclusive, return'
                ' all possible letter combinations that the number could'
                ' represent.'
            ),
            'def solution(digits):\n    # Write your solution here\n    pass\n',
            (
                'def solution(digits):\n    if not digits:\n        return'
                ' []\n    phone = {\n        \'2\': \'abc\', \'3\':'
                " 'def', '4': 'ghi', '5': 'jkl',\n        '6': 'mno', '7':"
                " 'pqrs', '8': 'tuv', '9': 'wxyz'\n    }\n    result = []\n   "
                ' def backtrack(index, current):\n        if index =='
                " len(digits):\n            result.append(''.join(current))\n  "
                '          return\n        for letter in'
                ' phone[digits[index]]:\n            current.append(letter)\n  '
                '          backtrack(index + 1, current)\n           '
                ' current.pop()\n    backtrack(0, [])\n    return result\n'
            ),
            json.dumps([
                {
                    'input': "solution('23')",
                    'expected': (
                        "['ad', 'ae', 'af', 'bd', 'be', 'bf', 'cd', 'ce', 'cf']"
                    ),
                },
                {'input': "solution('')", 'expected': '[]'},
            ]),
            'O(4^N) Time | O(N) Space',
        ),
    ]
    cursor.executemany(
        'INSERT INTO problems (title, category, difficulty, description,'
        ' starter_code, reference_solution, test_cases, complexity) VALUES (?, ?,'
        ' ?, ?, ?, ?, ?, ?)',
        sample_problems,
    )
    conn.commit()
  conn.close()


@app.route('/')
def index():
  conn = get_db_connection()
  problems = conn.execute('SELECT * FROM problems ORDER BY id DESC').fetchall()
  total = len(problems)
  passed_count = conn.execute(
      "SELECT COUNT(DISTINCT problem_id) FROM submissions WHERE status ="
      " 'Passed'"
  ).fetchone()[0]
  total_submissions = conn.execute(
      'SELECT COUNT(*) FROM submissions'
  ).fetchone()[0]
  conn.close()
  return render_template(
      'index.html',
      problems=problems,
      total=total,
      solved=passed_count,
      submissions=total_submissions,
  )


@app.route('/problem/<int:problem_id>')
def problem_detail(problem_id):
  conn = get_db_connection()
  problem = conn.execute(
      'SELECT * FROM problems WHERE id = ?', (problem_id,)
  ).fetchone()
  notes = conn.execute(
      'SELECT note_text FROM user_notes WHERE problem_id = ?', (problem_id,)
  ).fetchone()
  last_passed_submission = conn.execute(
      'SELECT code FROM submissions WHERE problem_id = ? AND status = '
      "'Passed' ORDER BY id DESC LIMIT 1",
      (problem_id,),
  ).fetchone()
  conn.close()

  if not problem:
    return redirect(url_for('index'))

  test_cases = (
      json.loads(problem['test_cases']) if problem['test_cases'] else []
  )
  saved_note = notes['note_text'] if notes else ''
  editor_code = (
      last_passed_submission['code']
      if last_passed_submission
      else problem['starter_code']
  )

  return render_template(
      'problem.html',
      problem=problem,
      editor_code=editor_code,
      test_cases=test_cases,
      saved_note=saved_note,
  )


@app.route('/api/fetch_next_random_problem', methods=['GET'])
def fetch_next_random_problem():
  import requests

  difficulties = ['EASY', 'MEDIUM', 'HARD']
  chosen_diff = random.choice(difficulties)

  leetcode_api_url = f'https://alfa-leetcode-api.onrender.com/problems?difficulty={chosen_diff}&limit=20'

  try:
    response = requests.get(leetcode_api_url, timeout=5)
    if response.status_code == 200:
      data = response.json()
      problem_list = data.get('problemsetQuestionList', [])

      if problem_list:
        selected = random.choice(problem_list)
        title = selected.get('title', 'LeetCode Challenge')
        difficulty = selected.get('difficulty', 'Easy').capitalize()

        tags = selected.get('topicTags', [])
        category = tags[0].get('name') if tags else 'Algorithms'

        description = (
            f'Solve LeetCode Problem: **{title}**.\n\nPractice optimizing'
            f' runtime and memory efficiency for this {difficulty}-level'
            ' challenge.'
        )

        # --- DYNAMIC GEMINI PROMPT (GEMINI 3.5 FLASH-LITE) ---
        prompt = f"""
        For the LeetCode problem '{title}' ({difficulty} level, category: {category}):

        Generate:
        1. `starter_code`: Python 3 function signature named `solution` with parameters and `pass`.
        2. `solution`: Full, complete, accurate working solution for function `solution`.
        3. `test_cases`: Exactly 2 test case objects with 'input' and 'expected' keys.

        CRITICAL EVALUATION RULES FOR TEST CASES:
        - The `expected` output MUST match Python `repr()` formatting.
        - For string returns, include quotes. Example: '"bab"' instead of 'bab'.
        - For array/list returns, stringify the list representation. Example: '[1, 2]'.
        - For integers/booleans, stringify directly. Example: '5' or 'True'.

        Return strictly valid JSON in this exact structure:
        {{
            "starter_code": "def solution(s: str) -> str:\\n    # Write your solution here\\n    pass",
            "solution": "def solution(s: str) -> str:\\n    # Complete optimal solution code...",
            "test_cases": [
                {{"input": "solution(\\\"babad\\\")", "expected": "\\\"bab\\\""}},
                {{"input": "solution(\\\"cbbd\\\")", "expected": "\\\"bb\\\""}}
            ]
        }}
        """

        try:
          ai_response = ai_client.models.generate_content(
              model='gemini-3.5-flash-lite',
              contents=prompt,
              config={'response_mime_type': 'application/json'},
          )

          ai_data = json.loads(ai_response.text)

          starter_code = ai_data.get(
              'starter_code', f'def solution(val):\n    pass\n'
          )
          ref_solution = ai_data.get(
              'solution',
              f'# AI generation failed for {title}. Write manually.',
          )

          raw_test_cases = ai_data.get('test_cases', [])
          formatted_test_cases = []
          for tc in raw_test_cases:
            formatted_test_cases.append({
                'input': str(tc.get('input', '')),
                'expected': str(tc.get('expected', '')),
            })

          test_cases = json.dumps(formatted_test_cases)

        except Exception as ai_err:
          print(f'\n❌ GEMINI API ERROR: {ai_err}\n')
          starter_code = f'def solution(val):\n    # Write solution for {title}\n    pass\n'
          ref_solution = f'# AI generation failed for {title}. Write manually.'
          test_cases = json.dumps([{'input': 'solution([])', 'expected': '0'}])

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO problems (title, category, difficulty, description,'
            ' starter_code, reference_solution, test_cases, complexity) VALUES'
            ' (?, ?, ?, ?, ?, ?, ?, ?)',
            (
                f'{title} (LeetCode)',
                category,
                difficulty,
                description,
                starter_code,
                ref_solution,
                test_cases,
                'O(N) Time | O(1) Space',
            ),
        )
        new_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return jsonify(
            {'redirect_url': url_for('problem_detail', problem_id=new_id)}
        )

  except Exception as e:
    print(f'⚠️ External API Timeout/Error: {e}')

  # --- LOCAL FALLBACK LOGIC ---
  conn = get_db_connection()
  existing_problems = conn.execute('SELECT id FROM problems').fetchall()
  conn.close()

  if existing_problems:
    random_id = random.choice(existing_problems)['id']
    return jsonify(
        {'redirect_url': url_for('problem_detail', problem_id=random_id)}
    )

  return jsonify({'redirect_url': url_for('index')})


@app.route('/api/run_code', methods=['POST'])
def run_code():
  data = request.get_json()
  code = data.get('code', '')
  problem_id = data.get('problem_id')

  conn = get_db_connection()
  problem = conn.execute(
      'SELECT * FROM problems WHERE id = ?', (problem_id,)
  ).fetchone()
  conn.close()

  if not problem:
    return jsonify({'status': 'Error', 'output': 'Problem context not found.'})

  test_cases = (
      json.loads(problem['test_cases']) if problem['test_cases'] else []
  )
  test_results = []
  all_passed = True

  for idx, tc in enumerate(test_cases, 1):
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    exec_globals = {}

    try:
      # Execute code and output formatted string matching repr()
      full_script = f"{code}\n\nresult = repr({tc['input']})\nprint(result)"
      exec(full_script, exec_globals)
      actual_output = redirected_output.getvalue().strip()

      expected_str = str(tc['expected'])

      # Normalize single/double quotes string matching
      if (
          actual_output.startswith("'")
          and actual_output.endswith("'")
          and expected_str.startswith('"')
          and expected_str.endswith('"')
      ):
        passed = actual_output[1:-1] == expected_str[1:-1]
      else:
        passed = actual_output == expected_str

      if not passed:
        all_passed = False

      test_results.append({
          'case': idx,
          'input': tc['input'],
          'expected': expected_str,
          'actual': actual_output,
          'passed': passed,
      })
    except Exception as e:
      all_passed = False
      test_results.append({
          'case': idx,
          'input': tc['input'],
          'expected': tc['expected'],
          'actual': f'Runtime Error: {str(e)}',
          'passed': False,
      })
    finally:
      sys.stdout = old_stdout

  status = 'Passed' if all_passed else 'Failed'

  conn = get_db_connection()
  conn.execute(
      'INSERT INTO submissions (problem_id, code, status, output) VALUES (?, ?,'
      ' ?, ?)',
      (problem_id, code, status, json.dumps(test_results)),
  )
  conn.commit()
  conn.close()

  return jsonify({
      'status': status,
      'results': test_results,
      'complexity': problem['complexity'] if all_passed else None,
  })


@app.route('/api/save_note', methods=['POST'])
def save_note():
  data = request.get_json()
  problem_id = data.get('problem_id')
  note_text = data.get('note_text', '')

  conn = get_db_connection()
  conn.execute(
      'INSERT OR REPLACE INTO user_notes (problem_id, note_text) VALUES (?, ?)',
      (problem_id, note_text),
  )
  conn.commit()
  conn.close()
  return jsonify({'success': True})


@app.route('/history')
def history():
  conn = get_db_connection()
  submissions = conn.execute(
      """SELECT s.*, p.title as problem_title 
           FROM submissions s 
           JOIN problems p ON s.problem_id = p.id 
           ORDER BY s.submitted_at DESC"""
  ).fetchall()
  conn.close()
  return render_template('history.html', submissions=submissions)


if __name__ == '__main__':
  init_db()
  app.run(debug=True, port=5000)