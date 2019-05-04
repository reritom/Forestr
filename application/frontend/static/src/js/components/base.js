//const SomeComponent = () => import('./tabs/some_component.js');

export default {
  name: "App",
  data: function () {
    return {
      something: false
    }
  },
  template: `<div>
                <!-- As a heading -->
                <nav class="navbar navbar-dark bg-dark">
                  <span class="navbar-brand mb-0 h1">ApplicationName</span>
                  <span class="mb-0 h2" v-html="TabName"></span>
                </nav>

                <p>This is your app</p>
            </div>`
};
