const login = new Vue({
    el: '#login',
    data: {
        email: '',
        password: '',
        remember: '',
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
                  password: this.password,
                  remember: this.remember
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