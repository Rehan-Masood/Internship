import numpy as np
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="CustomerChurn Intelligence Pro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --- DATA GENERATION & MODEL TRAINING ---
@st.cache_data
def load_and_train_model():
    np.random.seed(42)
    num_records = 1200

    tenure = np.random.randint(1, 72, size=num_records)
    monthly_charges = np.random.uniform(20.0, 120.0, size=num_records)
    support_tickets = np.random.poisson(lam=2, size=num_records)
    contract_type = np.random.choice(
        ["Month-to-Month", "One-Year", "Two-Year"],
        size=num_records,
        p=[0.6, 0.25, 0.15],
    )
    payment_method = np.random.choice(
        ["Credit Card", "Bank Transfer", "Electronic Check"], size=num_records
    )

    # Business Logic for Churn
    churn_score = (
        (72 - tenure) * 0.03
        + (monthly_charges / 120.0) * 0.4
        + (support_tickets * 0.18)
        + (contract_type == "Month-to-Month") * 0.55
    )
    churn_prob = 1 / (1 + np.exp(-churn_score + 2.5))
    churn = (churn_prob > 0.5).astype(int)

    df = pd.DataFrame(
        {
            "CustomerID": [f"CUST-{1000 + i}" for i in range(num_records)],
            "Tenure_Months": tenure,
            "Monthly_Charges": monthly_charges,
            "Support_Tickets": support_tickets,
            "Contract_Type": contract_type,
            "Payment_Method": payment_method,
            "Churn": churn,
        }
    )

    # Preprocessing
    X = df[
        [
            "Tenure_Months",
            "Monthly_Charges",
            "Support_Tickets",
            "Contract_Type",
            "Payment_Method",
        ]
    ]
    y = df["Churn"]
    X_encoded = pd.get_dummies(
        X, columns=["Contract_Type", "Payment_Method"], drop_first=True
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X_encoded, y, test_size=0.2, random_state=42, stratify=y
    )

    scaler = StandardScaler()
    num_cols = ["Tenure_Months", "Monthly_Charges", "Support_Tickets"]
    X_train[num_cols] = scaler.fit_transform(X_train[num_cols])
    X_test[num_cols] = scaler.transform(X_test[num_cols])

    model = RandomForestClassifier(
        n_estimators=100, random_state=42, max_depth=6
    )
    model.fit(X_train, y_train)

    acc = accuracy_score(y_test, model.predict(X_test))

    return df, model, scaler, X_encoded.columns, acc, X_test, y_test


df, model, scaler, feature_cols, accuracy, X_test, y_test = (
    load_and_train_model()
)

# --- SIDEBAR CONTROL PANEL ---
st.sidebar.title("📊 Control Center")
st.sidebar.markdown("---")
menu_choice = st.sidebar.radio(
    "Navigate Platform:",
    [
        "📈 Executive Dashboard (EDA)",
        "🤖 Live Churn Predictor",
        "⚙️ Model Performance",
    ],
)

# --- HEADER SECTION ---
st.title("🛡️ CustomerChurn Intelligence Pro")
st.caption(
    "Enterprise Machine Learning Engine for Predictive Analytics & Customer"
    " Retention"
)
st.markdown("---")

# --- TAB 1: EXECUTIVE DASHBOARD (EDA) ---
if menu_choice == "📈 Executive Dashboard (EDA)":
    st.subheader("📊 Key Business Metrics")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Accounts", f"{len(df):,}")
    col2.metric("Overall Churn Rate", f"{(df['Churn'].mean() * 100):.1f}%")
    col3.metric("Avg Tenure", f"{df['Tenure_Months'].mean():.1f} Months")
    col4.metric("Avg Monthly Spend", f"${df['Monthly_Charges'].mean():.2f}")

    st.markdown("### 🔍 Exploratory Data Analysis")

    c1, c2 = st.columns(2)

    with c1:
        fig_contract = px.histogram(
            df,
            x="Contract_Type",
            color="Churn",
            barmode="group",
            title="Churn Breakdown by Contract Type",
            color_discrete_sequence=["#10b981", "#ef4444"],
        )
        st.plotly_chart(fig_contract, width="stretch")

    with c2:
        fig_charges = px.box(
            df,
            x="Churn",
            y="Monthly_Charges",
            color="Churn",
            title="Monthly Charge Distribution by Churn Status",
            color_discrete_sequence=["#10b981", "#ef4444"],
        )
        st.plotly_chart(fig_charges, width="stretch")

# --- TAB 2: LIVE CHURN PREDICTOR ---
elif menu_choice == "🤖 Live Churn Predictor":
    st.subheader("🔮 Real-Time Customer Risk Evaluator")
    st.write("Adjust customer parameters below to calculate churn probability:")

    col_a, col_b = st.columns(2)

    with col_a:
        tenure_val = st.slider(
            "Tenure (Months)", min_value=1, max_value=72, value=12
        )
        monthly_val = st.slider(
            "Monthly Charges ($)", min_value=20.0, max_value=120.0, value=75.0
        )
        tickets_val = st.slider(
            "Support Tickets Opened", min_value=0, max_value=10, value=3
        )

    with col_b:
        contract_val = st.selectbox(
            "Contract Type", ["Month-to-Month", "One-Year", "Two-Year"]
        )
        payment_val = st.selectbox(
            "Payment Method", ["Electronic Check", "Credit Card", "Bank Transfer"]
        )

    # Format input for prediction
    input_dict = {
        "Tenure_Months": tenure_val,
        "Monthly_Charges": monthly_val,
        "Support_Tickets": tickets_val,
        "Contract_Type_One-Year": 1 if contract_val == "One-Year" else 0,
        "Contract_Type_Two-Year": 1 if contract_val == "Two-Year" else 0,
        "Payment_Method_Credit Card": 1 if payment_val == "Credit Card" else 0,
        "Payment_Method_Electronic Check": (
            1 if payment_val == "Electronic Check" else 0
        ),
    }

    input_df = pd.DataFrame([input_dict])

    # Ensure all feature columns match training columns
    for col in feature_cols:
        if col not in input_df.columns:
            input_df[col] = 0

    input_df = input_df[feature_cols]

    # Scale numerical columns
    num_cols = ["Tenure_Months", "Monthly_Charges", "Support_Tickets"]
    input_df[num_cols] = scaler.transform(input_df[num_cols])

    # Predict
    prob = model.predict_proba(input_df)[0][1] * 100

    st.markdown("---")
    st.subheader("🎯 Prediction Output")

    res_col1, res_col2 = st.columns([1, 2])

    with res_col1:
        st.metric("Predicted Churn Risk Score", f"{prob:.1f}%")

    with res_col2:
        if prob >= 65:
            st.error(
                "🚨 **HIGH CHURN RISK:** Immediate intervention recommended"
                " (Discount / Loyalty Outreach)."
            )
        elif prob >= 35:
            st.warning(
                "⚠️ **MEDIUM RISK:** Customer showing warning signs. Monitor"
                " tickets and engagement."
            )
        else:
            st.success(
                "✅ **LOW RISK:** Account in good standing with low probability"
                " of leaving."
            )

# --- TAB 3: MODEL PERFORMANCE ---
elif menu_choice == "⚙️ Model Performance":
    st.subheader("🤖 Machine Learning Model Diagnostic")

    st.metric("Model Accuracy (Random Forest)", f"{accuracy * 100:.2f}%")

    c1, c2 = st.columns(2)

    with c1:
        # Feature Importance Plot
        importances = pd.Series(
            model.feature_importances_, index=feature_cols
        ).sort_values(ascending=True)
        fig_imp = px.bar(
            importances,
            orientation="h",
            title="Feature Importances (Drivers of Churn)",
            labels={"value": "Relative Importance", "index": "Features"},
            color_discrete_sequence=["#06b6d4"],
        )
        st.plotly_chart(fig_imp, width="stretch")

    with c2:
        # Confusion Matrix
        y_pred = model.predict(X_test)
        cm = confusion_matrix(y_test, y_pred)
        fig_cm = ff.create_annotated_heatmap(
            z=cm,
            x=["Stayed", "Churned"],
            y=["Stayed", "Churned"],
            colorscale="Blues",
        )
        fig_cm.update_layout(title="Confusion Matrix")
        st.plotly_chart(fig_cm, width="stretch")
