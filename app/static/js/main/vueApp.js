let App;
var indexData;

AppCreate = () => {
    App = new Vue({
        el: '#app',
        data: {
            page: 'home',
            dados: {
                'nome': '',
                'registros': [],
                'arquivos': [],
                'servidores': [],
                'eventos': []
            },
            meses: ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'],
            dataAtual: null,
            modal: {
                active: false,
                title: 'Novo Servidor',
                bodyHTML: ``
            }
        },
        computed: {
            eventsList: function () {
                list = {};
                this.dados.eventos.forEach((evento) => {
                    indexData = vue_self.formatarDataHora(evento.data_inicio, 'DD/MM/YYYY');
                    (list[indexData] = list[indexData] || []).push(evento);
                })
                return list;
            }
        },
        methods: {
            getFirstName: function () {
                if (this.dados.hasOwnProperty('nome')) {
                    let nameArray = this.dados.nome.split(' ');
                    return nameArray[0]
                }
                return ''
            },
            getLastName: function () {
                if (this.dados.hasOwnProperty('nome')) {
                    let nameArray = this.dados.nome.split(' ');
                    return nameArray[nameArray.length - 1]
                }
                return ''
            },
            getDataExtenso: function () {
                let dia = this.dataAtual.getDate().toString().padStart(2, '0');
                let mes = this.meses[this.dataAtual.getMonth()];
                let ano = this.dataAtual.getFullYear();
                return `${dia} de ${mes} de ${ano}`
            },
            formatarDataHora: function (date, stringFormat) {
                var dataJS = new Date(date);
                var dia = dataJS.getUTCDate().toString().padStart(2, '0');
                var mes = (dataJS.getUTCMonth() + 1).toString().padStart(2, '0');
                var ano = (dataJS.getUTCFullYear()).toString().padStart(4, '0');
                var horas = (dataJS.getUTCHours()).toString().padStart(2, '0');
                var minutos = (dataJS.getUTCMinutes()).toString().padStart(2, '0');
                var segundos = dataJS.getUTCSeconds().toString().padStart(2, '0');
                var mesAbreviado = (this.meses[dataJS.getMonth()]).substring(0, 3) + '.';
                return stringFormat.replace('|M|', mesAbreviado).replace('DD', dia).replace('MM', mes).replace('YYYY', ano).replace('H', horas).replace('M', minutos).replace('S', segundos)
            },
            getFileClass: function (tipo) {
                if (tipo == 'pdf') {
                    return 'bx bxs-file-pdf'
                } else if (tipo.includes('xls')) {
                    return 'bx bxs-file icon-planilha'
                } else {
                    return 'bx bxs-file'
                }
            },
            openModal: async function (title, pathHTML, callback) {
                try {
                    let bodyHTML = await this.getHtmlModalFromPath(pathHTML);
                    let modal = `
                        <div id="overlay-modal">
                            <div id="modal">
                                <div class="top">
                                    <h3>${title}</h3>
                                    <button class="btn-close" onclick="App.closeModal(this)">⨉</button>
                                </div>
                                <div>
                                    ${bodyHTML}
                                </div>
                            </div>    
                        </div>
                    `;
                    $('#app').append(modal);
                    callback();
                } catch (error) {
                    console.error("Erro ao obter HTML do modal:", error);
                }
            },
            closeModal: function (modal) {
                console.log($(modal).parent().parent().parent().remove());
            },
            getHtmlModalFromPath: function (path) {
                return new Promise((resolve, reject) => {
                    $.get(`/getHTML/${path}`, function (data) {
                        resolve(data.html);
                    }).fail(function (error) {
                        reject(error);
                    });
                });
            },
            formServidores: function (id = null) {
                let title = 'Novo Servidor';
                let vue_self = this;
                let data = {
                    id: null,
                    nome: '',
                    email: '',
                    telefone: '',
                    cpf: '',
                    dataAdmissao: '',
                    cargo: '',
                    foto: '',
                    tipo: '',
                    tipoServidores: vue_self.dados.tipoServidores
                };

                if (id !== null) {
                    title = 'Editando Servidor'
                    let servidor = vue_self.dados.servidores.find((el) => el.id === id);
                    data.id = servidor.id;
                    data.nome = servidor.nome;
                    data.email = servidor.email;
                    data.telefone = servidor.telefone;
                    data.cpf = servidor.cpf;
                    data.dataAdmissao = this.formatarDataHora(servidor.data_admissao, 'YYYY-MM-DD');
                    data.cargo = servidor.cargo;
                    data.foto = servidor.foto;
                    data.tipo = servidor.id_tipo ?? "";
                }

                let callback = function () {
                    vueServidores = new Vue({
                        el: '#formServidores',
                        data: data,
                        methods: {
                            salvar: function (e) {
                                let vue_self = this;
                                e.preventDefault();
                                $.ajax({
                                    type: "POST",
                                    url: '/saveFuncionario',
                                    data: {
                                        id: vue_self.id,
                                        nome: vue_self.nome,
                                        email: vue_self.email,
                                        telefone: vue_self.telefone,
                                        cpf: vue_self.cpf,
                                        dataAdmissao: vue_self.dataAdmissao,
                                        cargo: vue_self.cargo,
                                        foto: vue_self.foto,
                                        tipo: vue_self.tipo
                                    },
                                    success: function (response) {
                                        if(response.success){
                                            window.location.reload();
                                        }
                                    },
                                    dataType: 'json'
                                });
                            }
                        }
                    });
                };

                this.openModal(title, 'formServidores.html', callback);
            },
            openMenuEditServidores: function (e) {
                e.stopPropagation();
                vue_self = this;
                let editContent = $(e.target).closest('.card').find('.edit-content');
                if(!editContent.hasClass('hidden')){
                    vue_self.closeMenuEditServidores();
                    return;
                }
                this.closeMenuEditServidores();
                editContent.toggleClass('hidden');
                $('body').on('click', (event) => {
                    this.closeMenuEditServidores();
                });
            },
            closeMenuEditServidores: function () {
                $('.edit-content').addClass('hidden');
                $('body').off('click');
            }

        },
        mounted() {
            vue_self = this;
            $.get('/getDados', function (response) {
                if (!response.logado) {
                    location.reload();
                }
                vue_self.dados = response.dados;
            })
            vue_self.dataAtual = new Date();
        },
        router
    }).$mount('#app');
}
