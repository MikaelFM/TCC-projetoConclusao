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
                'eventos': [],
                'tiposPrivacidade': [],
                'tipo' : ''
            },
            meses: ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'],
            dataAtual: null,
            modal: {
                active: false,
                title: 'Novo Servidor',
                bodyHTML: ``
            },
            filterServidores: {
                'orderBy': 'nome',
                'search' : ''
            },
            filterArquivos: {
                'orderBy': 'nome',
                'search' : ''
            }
        },
        computed: {
            eventsList: function () {
                list = {};
                this.dados.eventos.forEach((evento) => {
                    indexData = vue_self.formatarDataHora(evento.data, 'DD/MM/YYYY');
                    (list[indexData] = list[indexData] || []).push(evento);
                })
                return list;
            },
            servidoresFiltrados: function (){
                return this.filter(this.dados.servidores, this.filterServidores, 'nome')
            },
            arquivosFiltrados: function (){
                return this.filter(this.dados.arquivos, this.filterArquivos, 'nome')
            }
        },
        methods: {
            filter: function (toFilter, filterArray, fieldFilter){
                return toFilter.filter((el) =>
                    el[fieldFilter].toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "").
                    includes(filterArray.search.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, ""))).sort(function (a, b) {

                        fieldA = a[(filterArray['orderBy']).split('|')[0]] ?? '';
                        fieldB = b[(filterArray['orderBy']).split('|')[0]] ?? '';

                        switch ((filterArray['orderBy']).split('|')[1]){
                            case 'date':
                                fieldA = new Date(fieldA);
                                fieldB = new Date(fieldB);
                                break;
                            case 'number':
                                fieldA = parseFloat(fieldA);
                                fieldB = parseFloat(fieldB);
                                break;
                            default:
                                fieldA = fieldA.toString().toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
                                fieldB = fieldB.toString().toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
                                break;
                        }

                        if (typeof fieldA == 'string'){
                            if (fieldA > fieldB) {
                                return 1;
                            }
                            if (fieldA < fieldB) {
                                return -1;
                            }
                            return 0;
                        } else {
                            return fieldA - fieldB
                        }
                    })
            },
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
                if(typeof this.dataAtual !== 'undefined' && this.dataAtual != null){
                    let dia = this.dataAtual.getDate().toString().padStart(2, '0');
                    let mes = this.meses[this.dataAtual.getMonth()];
                    let ano = this.dataAtual.getFullYear();
                    return `${dia} de ${mes} de ${ano}`
                }
                return '';
            },
            formatarDataHora: function (date, stringFormat) {
                vue_self = this;
                let diasDaSemana = ['Domingo', 'Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado'];
                var dataJS = new Date(date);
                var dia = dataJS.getDate().toString().padStart(2, '0');
                var mes = (dataJS.getMonth() + 1).toString().padStart(2, '0');
                let mesExtenso = this.meses[dataJS.getMonth()];
                var ano = (dataJS.getFullYear()).toString().padStart(4, '0');
                var horas = (dataJS.getHours()).toString().padStart(2, '0');
                var minutos = (dataJS.getMinutes()).toString().padStart(2, '0');
                var segundos = dataJS.getSeconds().toString().padStart(2, '0');
                var mesAbreviado = (vue_self.meses[dataJS.getMonth()]).substring(0, 3) + '.';
                var diaDaSemana  = diasDaSemana[dataJS.getDay()]
                return stringFormat.replace('|M|', mesAbreviado).replace('DD', dia).replace('MM', mes).replace('YYYY', ano).replace('H', horas).replace('M', minutos).replace('S', segundos).replace('Dd', diaDaSemana).replace('mm', mesExtenso)
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
                                <div class="body-modal">
                                    <h3>${title}</h3>
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
            openModalConfirmation: function (title, msg, onConfirm) {
                let modal = `
                    <div id="overlay-modal">
                        <div id="modal" class="modal-confirmation">
                            <div class="top">
                                <button class="btn-close" onclick="App.closeModal(this)">⨉</button>
                            </div>
                            <div class="text">
                                <p>${msg}</p>
                            </div>
                            <div class="buttons">
                                <button class="button btn-cancel" onclick="App.closeModal(this)">Cancelar</button>
                                <button class="button btn-confirm" onclick="${onConfirm}">Confirmar</button>
                            </div>
                        </div>
                    </div>
                `;
                $('#app').append(modal);
            },
            openModalEvents: function (id, closeModalEventsList = true) {
                $('.modal-event').remove();
                if(closeModalEventsList){
                    $('.modal-events-list').remove();
                }
                let eventSelected = vue_self.dados.eventos.find((el) => el.id === id);
                let formatedDate = this.formatarDataHora(eventSelected.data, 'Dd, DD de mm de YYYY')
                let disabled = eventSelected.has_vinculo == 1 ? 'disabled' : ''
                event.stopPropagation();
                let elClicked = $(event.target);
                let buttons = "";
                if(eventSelected.can_edit == 1){
                    buttons = `
                        <button onclick="App.formEventos(${id})" ${disabled}>
                            <i class='bx bx-pencil'></i>
                        </button>
                        <button onclick="App.deleteEvento(${id})" ${disabled}> 
                            <i class='bx bx-trash'></i>
                        </button>`
                }
                let modal = `
                    <div id="modal" class="modal-event" style="opacity: 0; left: ${elClicked.offset().left}px; top: ${elClicked.offset().top}px">
                        <div class="top ${disabled}">
                            ${buttons}
                            <button class="btn-close" onclick="App.closeModal(this, false)">
                                ⨉
                            </button>
                        </div>
                        <div class="body">
                            <h3>${eventSelected.descricao}</h3>
                            <p>${formatedDate}</p>
                        </div>
                    </div>
                `;
                $('#app').append(modal);
                this.positionModal(event, '.modal-event')
            },
            openModalEventsList: function (date, fromHome = false) {
                $('.modal-event').remove();
                $('.modal-events-list').remove();
                let formatedDate = this.formatarDataHora(date, 'DD/MM/YYYY');
                let events = vue_self.eventsList[formatedDate] ?? [];
                let html = '';
                events.forEach((event) => {
                    let onClick = !fromHome ? `App.openModalEvents(${event.id}, false)` : ``;
                    let classe = fromHome ? 'event-none primary' : '';
                    html += `<div class="event from-event-list ${classe}" onclick="${onClick}"><p>${event.descricao}</p></div>`
                })
                if(html === ''){
                    html = `<div class="event event-none"><p>Sem eventos para esta data</p></div>`
                }

                let modal = `
                    <div id="modal" class="modal-events-list">
                        <div class="top">
                            <p>${formatedDate}</p>
                            <button class="btn-close" onclick="App.closeModal(this, false)">⨉</button>
                        </div>
                        <div class="events">
                            ${html}
                        </div>
                    </div>
                `;
                $('#app').append(modal);
                this.positionModal(event, '.modal-events-list');
            },
            positionModal: function (e, modalSelector){
                e.stopPropagation();
                let modal = $(modalSelector);
                let css = { 'opacity': 1 };
                let el = $(e.target);
                let gap = 7;
                let elMain = $('.agenda');

                let elReference = el.parent().parent();
                if(el.hasClass('from-event-list') || el.parent().hasClass('from-event-list')){
                    elReference = elReference.offsetParent()
                } else if (el.hasClass('from-ano-view') || el.hasClass('from-programacao-view') || el.hasClass('from-home')){
                    elReference = el
                    elMain = $('#body-page');
                } else if (el.hasClass('from-home-p')){
                    elReference = el.parent();
                    elMain = $('#body-page');
                }


                let trueWidthAgenda = parseFloat(((elMain).css('padding-left')).replace('px', '')) + (elMain).width() + parseFloat(((elMain).css('padding-right')).replace('px', ''))
                let trueHeightAgenda = parseFloat(((elMain).css('padding-top')).replace('px', ''))+ (elMain).height() + parseFloat(((elMain).css('padding-bottom')).replace('px', ''))

                let paddingLeftElReference = parseFloat((elReference.css('padding-left')).replace('px', ''));
                let paddingRightElReference = parseFloat((elReference.css('padding-right')).replace('px', ''));
                let paddingTopReference = parseFloat((elReference.css('padding-top')).replace('px', ''));
                let paddingBottomReference = parseFloat((elReference.css('padding-bottom')).replace('px', ''));

                let horizontalStartElReference = elReference.offset().left;
                let verticalStartElReference = elReference.offset().top;
                let horizontalEndElReference = horizontalStartElReference + paddingLeftElReference + elReference.width() + paddingRightElReference;
                let verticalEndElReference = verticalStartElReference + paddingTopReference + elReference.height() + paddingBottomReference;

                let horizontalMiddleElReferente = (horizontalStartElReference + horizontalEndElReference)/2
                let verticalMiddleElReferente = (verticalStartElReference + verticalEndElReference)/2

                let trueWidthModal = parseFloat((modal.css('padding-left')).replace('px', ''))+ modal.width() + parseFloat((modal.css('padding-right')).replace('px', ''))
                let trueHeightModal = parseFloat((modal.css('padding-top')).replace('px', ''))+ modal.height() + parseFloat((modal.css('padding-bottom')).replace('px', ''))

                let horizontalMiddle = $('#body-page').offset().left + ($('#body-page').width()/2);
                let verticalMiddle = $('#body-page').offset().top + ($('#body-page').height() / 2);

                if(horizontalMiddleElReferente < horizontalMiddle){
                     css['left'] = horizontalEndElReference + gap;
                }
                else {
                    css['left'] = horizontalStartElReference - gap - trueWidthModal + 'px'
                }

                if(verticalMiddleElReferente < verticalMiddle){
                     css['top'] = verticalStartElReference + gap + 'px'
                }
                else {
                    css['top'] = (verticalEndElReference - gap - trueHeightModal) + 'px'
                }

                modal.css(css)

                $(document).on('click', (ev) => {
                    var target = $(ev.target);
                    if (!modal.is(target) && modal.has(target).length === 0) {
                        modal.remove();
                        $(document).off('click');
                    }
                });
            },
            closeModal: function (modal, withOverlay = true) {
                let el = $(modal).parent().parent()
                if(withOverlay){
                    el = el.parent()
                }
                el.remove();
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
                    tipoServidores: vue_self.dados.tipoServidores,
                    inEdit: false,
                    msgError: ''
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
                    data.inEdit = true;
                }

                let callback = function () {
                    vueServidores = new Vue({
                        el: '#formServidores',
                        data: data,
                        computed: {
                            canSubmit: function () {
                                return !(
                                    (
                                        vue_self.empty(this.nome) ||
                                        vue_self.empty(this.email) ||
                                        vue_self.empty(this.telefone) ||
                                        vue_self.empty(this.cpf) ||
                                        vue_self.empty(this.dataAdmissao) ||
                                        vue_self.empty(this.cargo) ||
                                        vue_self.empty(this.tipo)
                                    )
                                )
                            }
                        },
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
                                        tipo: vue_self.tipo,
                                    },
                                    success: function (response) {
                                        if(response.success){
                                            window.location.reload();
                                        } else {
                                            vue_self.msgError = response.msg;
                                        }
                                    },
                                    dataType: 'json'
                                });
                            }
                        },
                        mounted(){
                             addValidations();
                        }
                    });
                };

                this.openModal(title, 'formServidores.html', callback);
            },
            deleteFuncionario: function (id) {
                let vue_self = this;
                $.ajax({
                    type: "POST",
                    url: '/deleteFuncionario',
                    data: {
                        id: id
                    },
                    success: function (response) {
                        if(response.success){
                            window.location.reload();
                        }
                    },
                    dataType: 'json'
                });
            },
            formEventos: function (id = null, date = null) {
                $('.modal-event').remove();
                let title = 'Novo Evento';
                let vue_self = this;
                let data = {
                    id: null,
                    descricao: '',
                    data: date != null ? this.formatarDataHora(date, 'YYYY-MM-DD') : '',
                    privacidade: '',
                    tiposPrivacidade: vue_self.dados.tiposPrivacidade
                };

                if (id !== null) {
                    title = 'Editando Evento'
                    let evento = vue_self.dados.eventos.find((el) => el.id === id);
                    data.id = evento.id;
                    data.descricao = evento.descricao;
                    data.data = evento.data.replace(' 00:00', '');
                    data.privacidade = evento.privacidade;
                }

                let callback = function () {
                    vueEventos = new Vue({
                        el: '#formEventos',
                        data: data,
                        computed: {
                            canSubmit: function () {
                                return !(
                                    (
                                        vue_self.empty(this.descricao) ||
                                        vue_self.empty(this.data) ||
                                        vue_self.empty(this.privacidade)
                                    )
                                )
                            }
                        },
                        methods: {
                            salvar: function (e) {
                                let vue_self = this;
                                e.preventDefault();
                                $.ajax({
                                    type: "POST",
                                    url: '/saveEvento',
                                    data: {
                                        id: vue_self.id,
                                        descricao: vue_self.descricao,
                                        data: vue_self.data,
                                        privacidade: vue_self.privacidade,
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

                this.openModal(title, 'formEventos.html', callback);
            },
            deleteEvento: function (id) {
                let vue_self = this;
                $.ajax({
                    type: "POST",
                    url: '/deleteEvento',
                    data: {
                        id: id
                    },
                    success: function (response) {
                        if(response.success){
                            window.location.reload();
                        }
                    },
                    dataType: 'json'
                });
            },
            formArquivos: function (id = null) {
                let title = 'Novo Arquivo';
                let vue_self = this;
                let data = {
                    id: null,
                    nome: '',
                    arquivo: [],
                    base64: ''
                };

                if (id !== null) {
                    title = 'Editando Arquivo'
                    let arquivo = vue_self.dados.arquivos.find((el) => el.id === id);
                    data.id = arquivo.id;
                    data.nome = arquivo.nome;
                    data.arquivo = arquivo.arquivo;
                    data.base64 = arquivo.base64
                }

                let callback = function () {
                    vueArquivo = new Vue({
                        el: '#formArquivos',
                        data: data,
                        computed: {
                            canSubmit: function () {
                                return !(
                                    (
                                        vue_self.empty(this.nome) ||
                                        vue_self.empty(this.arquivo) ||
                                        vue_self.empty(this.base64)
                                    )
                                )
                            }
                        },
                        methods: {
                            salvar: function (e) {
                                let vue_self = this;
                                let newData = {
                                    id: vue_self.id,
                                    nome: vue_self.nome,
                                }
                                if(vue_self.id == null){
                                    newData['arquivo'] = vue_self.base64;
                                    newData['tamanho'] = parseFloat(vue_self.arquivo.size/1000000).toFixed(2)
                                    newData['tipo']    = vue_self.arquivo.type.split('/')[1]
                                }
                                e.preventDefault();
                                $.ajax({
                                    type: "POST",
                                    url: '/saveArquivo',
                                    data: newData,
                                    success: function (response) {
                                        if(response.success){
                                            window.location.reload();
                                        }
                                    },
                                    dataType: 'json'
                                });
                            },
                            getFile: async function (e) {
                                e.preventDefault();
                                if (e.type === "change") {
                                    this.arquivo = e.target.files[0]
                                } else if (e.type === "drop") {
                                    this.arquivo = e.dataTransfer.files[0]
                                }
                                if (this.nome == "") {
                                    this.nome = this.arquivo.name;
                                }
                                this.base64 = await App.getBase64(this.arquivo);
                                $('#file-drop').removeClass('dragover');
                            }
                        },
                        mounted: function () {
                            const dropArea = $('#file-drop');

                              dropArea.on('dragenter dragover', function (e) {
                                e.preventDefault();
                                e.stopPropagation();
                                dropArea.addClass('dragover');
                              });

                              dropArea.on('dragleave drop', function (e) {
                                e.preventDefault();
                                e.stopPropagation();
                                dropArea.removeClass('dragover');
                              });

                              $('#fileInput').on('dragenter dragover drop', function (e) {
                                e.preventDefault();
                                e.stopPropagation();
                              });
                        }
                    });
                };

                this.openModal(title, 'formArquivos.html', callback);
            },
            downloadFile: function (id) {
                vue_self = this;
                let arquivo = vue_self.dados.arquivos.find((el) => el.id == id)
                const downloadLink = document.createElement("a");
                downloadLink.href = arquivo.arquivo;
                downloadLink.download = `${arquivo.nome}.${arquivo.tipo}`;
                downloadLink.click();
            },
            deleteFile: function (id) {
                let vue_self = this;
                $.ajax({
                    type: "POST",
                    url: '/deleteFile',
                    data: {
                        id: id
                    },
                    success: function (response) {
                        if(response.success){
                            window.location.reload();
                        }
                    },
                    dataType: 'json'
                });
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
            },
            getBase64: function(file) {
                return new Promise(
                    function(resolve, reject) {
                        const reader = new FileReader();
                        reader.onload = () => resolve(reader.result);
                        reader.onerror = () => reject();
                        reader.readAsDataURL(file);
                    }
                );
            },
            empty: function (val) {
                return val === undefined || val === null || val === ''
            },
            openMenu: function (){
                $('body').addClass('open-sidebar')
            },
            closeMenu: function (){
                $('body').removeClass('open-sidebar')
            },
            isPortrait: function () {
                return window.matchMedia("(orientation: portrait)").matches
            },
            openCloseNotification: function () {
                if($('.notifications-box').hasClass('active')){
                    $('.notifications-box').removeClass('active')
                    $('fa-bell').removeClass('active')
                } else {
                    $('.notifications-box').addClass('active')
                    $('fa-bell').addClass('active')
                }
            },
            getSaudacao: function () {
                if(this.dados.tipo == 'servidor'){
                    return `Olá, ${this.dados.nome.split(' ')[0]}!`
                } else {
                    let saudacao = '';
                    const hora = (new Date()).getHours();
                    if (hora >= 6 && hora < 12) {
                      saudacao = 'Bom dia!';
                    } else if (hora >= 12 && hora < 18) {
                      saudacao = 'Boa tarde!';
                    } else {
                      saudacao = 'Boa noite!';
                    }
                    return saudacao;
                }
            },
            getNameUser: function () {
                let nome = ''
                if(this.dados.tipo == 'servidor'){
                    let splitName = this.dados.nome.split(' ')
                    nome = `${splitName[0]} ${splitName[splitName.length - 1]}`
                }
                return nome;
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
            $(window).on('hashchange', function() {
                vue_self.closeMenu()
            });
            vue_self.dataAtual = new Date();

        },
        router
    }).$mount('#app');
}
