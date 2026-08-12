/**
 * =========================================================================
 * Inkwell — Cover Image Validator
 * Client-side validation for blog cover images
 * Validates: resolution, aspect ratio, file type, file size
 * =========================================================================
 */

const ImageValidator = {
  // Validation constraints
  constraints: {
    minResolution: { width: 800, height: 450 },
    recommendedResolution: { width: 1280, height: 720 },
    maxResolution: { width: 1920, height: 1080 },
    aspectRatio: 16 / 9,
    aspectRatiaTolerance: 0.05, // 5% tolerance
    maxFileSize: 5 * 1024 * 1024, // 5 MB in bytes
    allowedFormats: ['image/jpeg', 'image/png', 'image/webp'],
    allowedExtensions: ['jpg', 'jpeg', 'png', 'webp'],
  },

  /**
   * Validate a selected image file
   * @param {File} file - The selected file
   * @param {Function} onValid - Callback if valid
   * @param {Function} onInvalid - Callback if invalid, receives error object
   */
  validateFile(file, onValid, onInvalid) {
    // Step 1: Check file type
    if (!this.isValidFileType(file)) {
      onInvalid({
        type: 'format',
        message: 'Unsupported Image Format',
        details: `Only JPG, JPEG, PNG, and WebP images are supported.`,
        allowed: 'JPG / JPEG / PNG / WebP',
      });
      return;
    }

    // Step 2: Check file size
    if (file.size > this.constraints.maxFileSize) {
      onInvalid({
        type: 'fileSize',
        message: 'File Size Too Large',
        details: `Your image is ${this.formatFileSize(file.size)}, which exceeds the maximum allowed size.`,
        maxSize: this.formatFileSize(this.constraints.maxFileSize),
        actualSize: this.formatFileSize(file.size),
      });
      return;
    }

    // Step 3: Load image and check dimensions
    this.loadImage(file, (img) => {
      const validation = this.validateDimensions(img.naturalWidth, img.naturalHeight);

      if (validation.valid) {
        onValid();
      } else {
        onInvalid(validation.error);
      }
    });
  },

  /**
   * Validate image dimensions and aspect ratio
   * @param {number} width - Image width in pixels
   * @param {number} height - Image height in pixels
   * @returns {Object} { valid: boolean, error?: Object }
   */
  validateDimensions(width, height) {
    const min = this.constraints.minResolution;
    const max = this.constraints.maxResolution;
    const targetRatio = this.constraints.aspectRatio;
    const tolerance = this.constraints.aspectRatiaTolerance;

    // Check minimum resolution
    if (width < min.width || height < min.height) {
      return {
        valid: false,
        error: {
          type: 'tooSmall',
          message: 'Image Resolution Too Low',
          details: `Your image is ${width} × ${height} px, which is below the minimum required resolution.`,
          actual: `${width} × ${height} px`,
          minimum: `${min.width} × ${min.height} px`,
          recommended: `${this.constraints.recommendedResolution.width} × ${this.constraints.recommendedResolution.height} px`,
          maximum: `${max.width} × ${max.height} px`,
          aspectRatio: '16:9',
        },
      };
    }

    // Check maximum resolution
    if (width > max.width || height > max.height) {
      return {
        valid: false,
        error: {
          type: 'tooLarge',
          message: 'Image Resolution Too High',
          details: `Your image is ${width} × ${height} px, which exceeds the maximum allowed resolution.`,
          actual: `${width} × ${height} px`,
          minimum: `${min.width} × ${min.height} px`,
          recommended: `${this.constraints.recommendedResolution.width} × ${this.constraints.recommendedResolution.height} px`,
          maximum: `${max.width} × ${max.height} px`,
          aspectRatio: '16:9',
        },
      };
    }

    // Check aspect ratio
    const actualRatio = width / height;
    const difference = Math.abs(actualRatio - targetRatio);
    const allowedDifference = targetRatio * tolerance;

    if (difference > allowedDifference) {
      return {
        valid: false,
        error: {
          type: 'wrongRatio',
          message: 'Unsupported Aspect Ratio',
          details: `Your image is ${width} × ${height} px with a ${(actualRatio).toFixed(2)}:1 ratio. Inkwell cover images require a 16:9 aspect ratio.`,
          actual: `${width} × ${height} px (${(actualRatio).toFixed(2)}:1)`,
          minimum: `${min.width} × ${min.height} px`,
          recommended: `${this.constraints.recommendedResolution.width} × ${this.constraints.recommendedResolution.height} px`,
          maximum: `${max.width} × ${max.height} px`,
          aspectRatio: '16:9',
        },
      };
    }

    // All validations passed
    return { valid: true };
  },

  /**
   * Check if file type is valid
   * @param {File} file - The file to check
   * @returns {boolean}
   */
  isValidFileType(file) {
    // Check MIME type
    if (!this.constraints.allowedFormats.includes(file.type)) {
      return false;
    }

    // Double-check with file extension
    const extension = file.name.split('.').pop().toLowerCase();
    return this.constraints.allowedExtensions.includes(extension);
  },

  /**
   * Load an image file and execute callback with the loaded image
   * @param {File} file - The image file
   * @param {Function} callback - Called with the loaded image element
   */
  loadImage(file, callback) {
    const reader = new FileReader();

    reader.onload = (e) => {
      const img = new Image();
      img.onload = () => callback(img);
      img.onerror = () => {
        // If image fails to load, consider it invalid
        callback({ naturalWidth: 0, naturalHeight: 0 });
      };
      img.src = e.target.result;
    };

    reader.onerror = () => {
      // If file read fails, consider it invalid
      callback({ naturalWidth: 0, naturalHeight: 0 });
    };

    reader.readAsDataURL(file);
  },

  /**
   * Format file size for display
   * @param {number} bytes - File size in bytes
   * @returns {string}
   */
  formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
  },
};

/**
 * Initialize cover image validation on page load
 */
document.addEventListener('DOMContentLoaded', function () {
  const coverImageInput = document.getElementById('cover_image');
  const validationModal = document.getElementById('image-validation-modal');
  const modalClose = document.querySelector('[data-modal-close-image-validator]');
  const modalChooseAnother = document.getElementById('modal-choose-another');

  if (!coverImageInput) return; // Not on a page with cover image upload

  /**
   * Handle file selection
   */
  coverImageInput.addEventListener('change', function (e) {
    const file = e.target.files[0];

    if (!file) return; // No file selected

    ImageValidator.validateFile(
      file,
      // Valid callback
      () => {
        // Image is valid - allow the existing upload process to continue
        // Reset any previous errors
        const errorContainer = coverImageInput.parentElement.querySelector('.form-error');
        if (errorContainer) {
          errorContainer.remove();
        }
        // Form will submit normally
      },
      // Invalid callback
      (error) => {
        // Image is invalid - show validation modal
        showValidationModal(error);
        // Reset the file input so the invalid image is not submitted
        coverImageInput.value = '';
      }
    );
  });

  /**
   * Show the premium validation modal
   */
  function showValidationModal(error) {
    if (!validationModal) return;

    // Update modal content based on error type
    const modalTitle = validationModal.querySelector('[data-modal-title]');
    const modalMessage = validationModal.querySelector('[data-modal-message]');
    const modalDetails = validationModal.querySelector('[data-modal-details]');

    if (modalTitle) {
      modalTitle.textContent = error.message;
    }

    if (modalMessage) {
      modalMessage.innerHTML = `
        <div class="image-validator-error-detail">
          <div class="image-validator-actual">
            <span class="image-validator-label">Your Image</span>
            <span class="image-validator-value">${error.actual || 'Unknown'}</span>
          </div>
        </div>
        <p>${error.details || 'Please check your image and try again.'}</p>
        <div class="image-validator-requirements">
          <div class="image-validator-req">
            <span class="image-validator-label">Minimum:</span>
            <span class="image-validator-value">${error.minimum || 'N/A'}</span>
          </div>
          <div class="image-validator-req">
            <span class="image-validator-label">Recommended:</span>
            <span class="image-validator-value">${error.recommended || 'N/A'}</span>
          </div>
          <div class="image-validator-req">
            <span class="image-validator-label">Maximum:</span>
            <span class="image-validator-value">${error.maximum || 'N/A'}</span>
          </div>
          ${error.aspectRatio ? `
          <div class="image-validator-req">
            <span class="image-validator-label">Aspect Ratio:</span>
            <span class="image-validator-value">${error.aspectRatio}</span>
          </div>
          ` : ''}
          ${error.maxSize ? `
          <div class="image-validator-req">
            <span class="image-validator-label">Max File Size:</span>
            <span class="image-validator-value">${error.maxSize}</span>
          </div>
          ` : ''}
        </div>
      `;
    }

    if (modalDetails) {
      modalDetails.textContent = 'Please resize or re-export your image and try again.';
    }

    // Show the modal
    validationModal.classList.add('is-open');
  }

  /**
   * Close modal handlers
   */
  if (modalClose) {
    modalClose.addEventListener('click', () => {
      validationModal.classList.remove('is-open');
    });
  }

  if (modalChooseAnother) {
    modalChooseAnother.addEventListener('click', () => {
      validationModal.classList.remove('is-open');
      // Focus back on the file input for accessibility
      coverImageInput.focus();
    });
  }

  // Close modal when clicking the backdrop
  const backdrop = validationModal?.querySelector('.inkwell-modal-backdrop');
  if (backdrop) {
    backdrop.addEventListener('click', () => {
      validationModal.classList.remove('is-open');
    });
  }

  // Close modal with Escape key
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && validationModal?.classList.contains('is-open')) {
      validationModal.classList.remove('is-open');
    }
  });
});
