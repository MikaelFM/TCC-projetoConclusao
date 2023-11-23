const register = new Vue({
    el: '#register',
    data: {
        nome: '',
        cpf: '',
        telefone: '',
        email: '',
        password: '',
        confirmPassword: '',
        msgError: ''
    },
    methods: {
        submit: function (e) {
            let vue_instance = this;
            e.preventDefault();
            $.ajax({
              type: "POST",
              url: '/registerSubmit',
              data: {
                   nome: this.nome,
                   cpf: this.cpf,
                   telefone: this.telefone,
                   email: this.email,
                   password: this.password,
                   confirmPassword: this.confirmPassword,
              },
              success: function (response) {
                  if(!response.success){
                      vue_instance.msgError = response.msg;
                  } else {
                      $('form').submit();
                  }
              },
              dataType: 'json'
            });
        }
    }
})