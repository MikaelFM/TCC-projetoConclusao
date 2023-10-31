const login = new Vue({
    el: '#login',
    delimiters: ['[[', ']]'],
    data: {
        email: '',
        password: '',
        msgError: ''
    },
    methods: {
        submit: function (e) {
            let vue_instance = this;
            e.preventDefault();
            $.ajax({
              type: "POST",
              url: '/loginSubmit',
              data: {
                  email: this.email,
                  password: this.password
              },
              success: function (response) {
                  if(!response.success){
                      vue_instance.msgError = response.msg;
                  } else {
                      if(response.confirmarEmail){
                          let form = document.getElementById('form-login');
                          form.submit()
                      } else {
                          window.location.href = '/'
                      }
                  }
              },
              dataType: 'json'
            });
        }
    }
})