<template>
  <div class="container">
    <header>
      <h1>Templates we recommend for entry-level</h1>
      <p>You can always change your template later.</p>
    </header>

    <div class="filters">
      <div class="filter">
        <label for="headshot">Filters:</label>
        <select id="headshot">
          <option value="headshot">Headshot</option>
        </select>
      </div>
      <div class="filter">
        <label for="graphics">Graphics:</label>
        <select id="graphics">
          <option value="graphics">Graphics</option>
        </select>
      </div>
      <div class="filter">
        <label for="columns">Columns:</label>
        <select id="columns">
          <option value="columns">Columns</option>
        </select>
      </div>
      <div class="filter colors">
        <label>Color:</label>
        <div class="color-option" style="background-color: #ffffff;"></div>
        <div class="color-option" style="background-color: #e0e0e0;"></div>
        <div class="color-option" style="background-color: #a0a0a0;"></div>
        <div class="color-option" style="background-color: #606060;"></div>
        <div class="color-option" style="background-color: #000000;"></div>
        <div class="color-option" style="background-color: #0066cc;"></div>
        <div class="color-option" style="background-color: #009688;"></div>
        <div class="color-option" style="background-color: #f57c00;"></div>
      </div>
    </div>

    <div class="templates">
      <div class="template">
        <img src="/src/assets/images/blog/blog-img1.jpg" alt="Template 1">
        <p>Venses Resume</p>
      </div>
      <div class="template">
        <img src="/src/assets/images/blog/blog-img2.jpg" alt="Template 2">
        <p>Pandy Resume</p>
      </div>
      <div class="template">
        <img src="/src/assets/images/blog/blog-img3.jpg" alt="Template 3">
        <p>Diya Resume</p>
      </div>
    </div>

    <footer>
      <button class="skip">Skip for now</button>
      <button @click="chooseTemplate" class="choose-template">Choose this template</button>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'TemplateSelection',
  methods: {
    chooseTemplate() {
      this.$router.push({ name: 'Resumeupload' });
    }
  }
};
</script>


<style scoped>
/* Add your styles here */
</style>