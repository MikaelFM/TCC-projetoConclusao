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
    computed: {
        canSubmit: function () {
            if(this.password != ''){
                if(!this.passSecure()){
                    this.msgError = "Certifique-se de a senha tenha pelo menos 8 caracteres, incluindo um número, uma letra minúscula e um caractere especial";
                } else {
                    if(this.password != this.confirmPassword){
                        this.msgError = "As senhas não conferem";
                    } else {
                        this.msgError = "";
                    }
                }
            }
            return !(
                (
                    this.empty(this.nome) ||
                    this.empty(this.cpf) ||
                    this.empty(this.telefone) ||
                    this.empty(this.email) ||
                    this.empty(this.password) ||
                    this.empty(this.confirmPassword) ||
                    this.password !== this.confirmPassword ||
                    !this.passSecure
                )
            )
        },
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
                    if (!response.success) {
                        vue_instance.msgError = response.msg;
                    } else {
                        $('form').submit();
                    }
                },
                dataType: 'json'
            });
        },
        empty: function (val) {
            return val === undefined || val === null || val === ''
        },
        passSecure: function () {
            if (this.password.length < 8) {
                return false;
            }

            if (!/[a-z]/.test(this.password)) {
                return false;
            }

            if (!/[A-Z]/.test(this.password)) {
                return false;
            }

            if (!/\d/.test(this.password)) {
                return false;
            }

            if (!/[!@#$%^&*()_+{}\[\]:;<>,.?~\\/-]/.test(this.password)) {
                return false;
            }

            return true;
        }
    },
    watch: {
        'password': function () {
            if(!this.passSecure){
                this.msgError = "Certifique-se de a senha tenha pelo menos 8 caracteres, incluindo um número, uma letra minúscula e um caractere especial";
            } else {
                this.msgError = ""
            }
        }
    },
    mounted() {
        addValidations();
    }
})