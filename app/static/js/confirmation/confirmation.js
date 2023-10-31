const confirmation = new Vue({
    el: '#el-main',
    delimiters: ['[[', ']]'],
    data: {
        email: email,
        sented: false,
        buttonDisabled: false,
        time: 59,
        txtButton: `Enviar e-mail de confirmação`,
        corrigir: false
    },
    methods: {
        sendEmail: function () {
            let vue_instance = this
            vue_instance.buttonDisabled = true;
            vue_instance.txtButton = 'Enviando, aguarde'
            $.ajax({
              type: "POST",
              url: '/sendConfirmation',
              data: {
                  email: vue_instance.email
              },
              success: function (response) {
                  if(!response.success){
                      console.log(response.msg);
                  } else {
                      vue_instance.txtButton = `Reenviar e-mail de confirmação`
                      vue_instance.sented = true;
                      vue_instance.timerActivate()
                  }
              },
              dataType: 'json'
            });
        },
        timerActivate: function () {
            let vue_instance = this
            if(vue_instance.buttonDisabled){
                vue_instance.time -= 1
                let timer = setInterval(function () {
                    vue_instance.time -= 1
                    if(vue_instance.time === 0){
                        vue_instance.time = 60;
                        vue_instance.buttonDisabled = false;
                        clearInterval(timer);
                    }
                }, 1000)
            }
        },
        setCorrigir: function () {
            this.corrigir = true;
        },
        cancelCorrigir: function (e) {
            e.preventDefault();
            this.corrigir = false;
        }
    },
});
