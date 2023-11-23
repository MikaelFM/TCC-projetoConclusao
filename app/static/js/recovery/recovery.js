const recovery = new Vue({
    el: '#recovery',
    data: {
        email: '',
        notExists: false,
        sented: false,
        error: false,
        buttonDisabled: false,
    },
    methods: {
        submit: function (e) {
            let vue_instance = this;
            e.preventDefault();
            if(!vue_instance.buttonDisabled){
                $.ajax({
                  type: "POST",
                  url: '/checkEmailExists',
                  data: {
                      email: this.email
                  },
                  success: function (response) {
                      if(!response.exists){
                          vue_instance.notExists = true;
                      } else {
                          vue_instance.buttonDisabled = true;
                          $.ajax({
                              type: "POST",
                              url: '/sendRecovery',
                              data: {
                                  email: vue_instance.email
                              },
                              success: function (response) {
                                  vue_instance.buttonDisabled = false;
                                  if(response.success){
                                      vue_instance.sented = true;
                                  } else {
                                      vue_instance.sented = true;
                                      vue_instance.error = true;
                                  }
                              },
                              error: function (response) {
                                  vue_instance.buttonDisabled = false;
                                  vue_instance.sented = true;
                                  vue_instance.error = true;
                              },
                              dataType: 'json'
                          });
                      }
                  },
                  dataType: 'json'
                });
            }
        }
    }
})