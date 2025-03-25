// backend/static/js/form.js

class LocationFormHandler {
    constructor() {
      this.countrySelect = document.getElementById('country');
      this.stateSelect = document.getElementById('state');
      this.citySelect = document.getElementById('city');
      this.loadingIndicator = this.createLoadingIndicator();
      this.errorContainer = this.createErrorContainer();
      this.cachedLocations = null;
      this.retryCount = 0;
      this.maxRetries = 3;
  
      this.initialize();
    }
  
    initialize() {
      this.injectUIElements();
      this.setupEventListeners();
      this.loadLocations();
    }
  
    injectUIElements() {
      document.body.appendChild(this.loadingIndicator);
      document.body.appendChild(this.errorContainer);
    }
  
    createLoadingIndicator() {
      const loader = document.createElement('div');
      loader.id = 'loading-indicator';
      loader.className = 'hidden fixed top-4 right-4 bg-slate-800 p-4 rounded-lg shadow-lg';
      loader.innerHTML = `
        <div class="flex items-center">
          <svg class="animate-spin h-5 w-5 text-purple-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span class="ml-2">Loading locations...</span>
        </div>
      `;
      return loader;
    }
  
    createErrorContainer() {
      const container = document.createElement('div');
      container.id = 'error-container';
      container.className = 'hidden fixed top-4 right-4 bg-red-800 p-4 rounded-lg shadow-lg max-w-md';
      return container;
    }
  
    async loadLocations() {
      try {
        this.showLoading();
        
        if (this.cachedLocations) {
          this.populateCountries();
          return;
        }
  
        const response = await fetch('/locations');
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        
        const data = await response.json();
        if (!Array.isArray(data)) throw new Error('Invalid location data format');
  
        this.cachedLocations = data;
        this.populateCountries();
        this.hideError();
      } catch (error) {
        this.handleError(error);
      } finally {
        this.hideLoading();
      }
    }
  
    populateCountries() {
      this.clearSelect(this.countrySelect);
      const countries = [...new Set(this.cachedLocations.map(item => item.country).filter(Boolean))].sort();
      
      // Add default option with ARIA attributes
      const defaultOption = new Option('Select Country', '');
      defaultOption.setAttribute('aria-label', 'Select a country');
      this.countrySelect.add(defaultOption);
      
      // Add country options with ARIA attributes
      countries.forEach(country => {
        const option = new Option(country, country);
        option.setAttribute('aria-label', `Select ${country}`);
        this.countrySelect.add(option);
      });
      
      this.countrySelect.disabled = false;
      this.countrySelect.setAttribute('aria-busy', 'false'); // Indicate loading is complete
    }
  
    populateStates(selectedCountry) {
      this.clearSelect(this.stateSelect);
      this.stateSelect.disabled = true;
      this.stateSelect.setAttribute('aria-busy', 'true'); // Indicate loading is in progress
      
      const states = [...new Set(this.cachedLocations
        .filter(item => item.country === selectedCountry)
        .map(item => item.state)
        .filter(Boolean)
      )].sort();
  
      // Add default option with ARIA attributes
      const defaultOption = new Option('Select State', '');
      defaultOption.setAttribute('aria-label', 'Select a state');
      this.stateSelect.add(defaultOption);
      
      // Add state options with ARIA attributes
      states.forEach(state => {
        const option = new Option(state, state);
        option.setAttribute('aria-label', `Select ${state}`);
        this.stateSelect.add(option);
      });
      
      this.stateSelect.disabled = false;
      this.stateSelect.setAttribute('aria-busy', 'false'); // Indicate loading is complete
    }
  
    populateCities(selectedCountry, selectedState) {
      this.clearSelect(this.citySelect);
      this.citySelect.disabled = true;
      this.citySelect.setAttribute('aria-busy', 'true'); // Indicate loading is in progress
      
      const cities = this.cachedLocations
        .filter(item => item.country === selectedCountry && item.state === selectedState)
        .map(item => item.city)
        .filter(Boolean)
        .sort();
  
      // Add default option with ARIA attributes
      const defaultOption = new Option('Select City', '');
      defaultOption.setAttribute('aria-label', 'Select a city');
      this.citySelect.add(defaultOption);
      
      // Add city options with ARIA attributes
      cities.forEach(city => {
        const option = new Option(city, city);
        option.setAttribute('aria-label', `Select ${city}`);
        this.citySelect.add(option);
      });
      
      this.citySelect.disabled = false;
      this.citySelect.setAttribute('aria-busy', 'false'); // Indicate loading is complete
    }
  
    clearSelect(selectElement) {
      while (selectElement.options.length > 0) {
        selectElement.remove(0);
      }
    }
  
    // Input Validation Helper
    validateSelections() {
      const errors = [];
  
      // Validate country
      if (!this.countrySelect.value) {
        errors.push('Please select a country.');
        this.countrySelect.setAttribute('aria-invalid', 'true');
      } else {
        this.countrySelect.setAttribute('aria-invalid', 'false');
      }
  
      // Validate state
      if (!this.stateSelect.value) {
        errors.push('Please select a state.');
        this.stateSelect.setAttribute('aria-invalid', 'true');
      } else {
        this.stateSelect.setAttribute('aria-invalid', 'false');
      }
  
      // Validate city
      if (!this.citySelect.value) {
        errors.push('Please select a city.');
        this.citySelect.setAttribute('aria-invalid', 'true');
      } else {
        this.citySelect.setAttribute('aria-invalid', 'false');
      }
  
      return errors;
    }
  
    setupEventListeners() {
      this.countrySelect.addEventListener('change', () => {
        const selectedCountry = this.countrySelect.value;
        this.stateSelect.disabled = true;
        this.citySelect.disabled = true;
        
        if (selectedCountry) {
          this.populateStates(selectedCountry);
        }
      });
  
      this.stateSelect.addEventListener('change', () => {
        const selectedCountry = this.countrySelect.value;
        const selectedState = this.stateSelect.value;
        
        if (selectedCountry && selectedState) {
          this.populateCities(selectedCountry, selectedState);
        }
      });
  
      // Add form submission validation
      const form = document.querySelector('form');
      form.addEventListener('submit', (e) => {
        const errors = this.validateSelections();
        
        if (errors.length > 0) {
          e.preventDefault(); // Prevent form submission
          this.showError(errors.join('<br>')); // Show all errors
        }
      });
    }
  
    handleError(error) {
      console.error('Location loading error:', error);
      this.retryCount++;
      
      if (this.retryCount <= this.maxRetries) {
        setTimeout(() => this.loadLocations(), 2000);
        this.showError(`Failed to load locations. Retrying (${this.retryCount}/${this.maxRetries})...`);
      } else {
        this.showError('Failed to load location data. Please try refreshing the page.');
        this.countrySelect.disabled = true;
      }
    }
  
    showError(message) {
      this.errorContainer.innerHTML = message; // Use innerHTML to support <br> tags
      this.errorContainer.classList.remove('hidden');
    }
  
    hideError() {
      this.errorContainer.classList.add('hidden');
    }
  
    showLoading() {
      this.loadingIndicator.classList.remove('hidden');
    }
  
    hideLoading() {
      this.loadingIndicator.classList.add('hidden');
    }
  }
  
  // Initialize when DOM is ready
  document.addEventListener('DOMContentLoaded', () => {
    new LocationFormHandler();
  });