const inputEmail = new Vue({
    el: '#input-email',
    delimiters: ['[[', ']]'],
    data: {
        email: '',
        error: false
    },
    methods: {
        submit: function (e) {
            let vue_instance = this;
            e.preventDefault();
            $.ajax({
              type: "POST",
              url: '/checkEmailExists',
              data: {
                  email: this.email,
              },
              success: function (response) {
                  if(!response.exists){
                      vue_instance.error = true;
                  } else {
                      let form = $('form');
                      form.submit()
                  }
              },
              dataType: 'json'
            });
        }
    }
})