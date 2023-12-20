Vue.component('calendar-home', {
    extends: calendarBase,
});

Vue.component('calendar-agenda', {
    extends: calendarBase,
    template: `
            <router-linkrticle>
                <div class="header">
                    <div class="flex-content">
                        <button class="today button" @click="hoje()">Hoje</button>
                        <div class="arrows" v-if="isMesView() || isAnoView()">
                            <button class="back" @click="back()"><</button>
                            <button class="front" @click="pass()">></button> 
                        </div>
                        <div class="date">
                            <div class="text">
                                <h1>Agenda</h1>
                            </div>
                            <p class="mes" v-if="isMesView()">{{ meses[getMes()] }} {{ getAno() }}</p>
                            <p class="mes" v-if="isAnoView()">{{ calendarioAno }}</p>
                        </div>
                        <div class="right-buttons">
                            <select class="button" v-model="modelo">
                                <option value="mes-active">Mês</option>
                                <option value="ano-active">Ano</option>
                                <option value="programacao-active">Programação</option>
                            </select>
                            <button class="button novo" @click="$root.formEventos()">Novo Evento</button>
                        </div>
                    </div>
                    <div class="mes-header" v-if="isMesView()">
                        <p>Dom</p>
                        <p>Seg</p>
                        <p>Ter</p>
                        <p>Qua</p>
                        <p>Qui</p>
                        <p>Sex</p>
                        <p>Sáb</p>
                    </div>
                </div>
                <div class="agenda">
                    <div class="mes-view" v-if="isMesView()">
                        <div class="dia" v-for="(item, key) in arrayDatas">
                            <p class="numero-dia" :class="{'gray' : item.getMonth() !== getMes()}">{{item.getDate()}}</p>
                            <div v-if="getEventsDay(item).length <= 2">
                                <div class="event" v-for="(evento) in getEventsDay(item)" @click="$root.openModalEvents(evento.id)">{{evento.descricao}}</div>
                            </div>
                            <div v-else>
                                <div class="event" @click="$root.openModalEvents(getEventsDay(item)[0]['id'])">{{(getEventsDay(item)[0]).descricao}}</div>
                                <div class="event button from-button-day" @click="$root.openModalEventsList(item)">Mais {{getEventsDay(item).length - 1}}</div>
                            </div>
                        </div>
                    </div>
                    <div class="ano-view" v-if="isAnoView()">
                        <div class="mes" v-for="(mes, key) in arrayAno">
                            <div class="mes-header">
                                <div class="nome">{{meses[key]}}</div>
                            </div>
                            <div class="grid-dias">
                                <div class="dia">
                                    <p class="numero name">D</p>
                                </div>
                                <div class="dia">
                                    <p class="numero name">S</p>
                                </div>
                                <div class="dia">
                                    <p class="numero name">T</p>
                                </div>
                                <div class="dia">
                                    <p class="numero name">Q</p>
                                </div>
                                <div class="dia">
                                    <p class="numero name">Q</p>
                                </div>
                                <div class="dia">
                                    <p class="numero name">S</p>
                                </div>
                                <div class="dia">
                                    <p class="numero name">S</p>
                                </div>
                                <div class="dia from-ano-view" v-for="dia in mes" :class="{'with-events' : getEventsDay(dia).length > 0 && dia.getMonth() === key}" @click="$root.openModalEventsList(dia)">
                                    <div class="dia-background">
                                        <p 
                                            class="numero" 
                                            :class="{'gray' : dia.getMonth() !== key}"
                                        >
                                            {{dia.getDate()}}
                                        </p>             
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="programacao-view" v-if="isProgramacaoView()">
                        <div class="evento" v-for="(diaEvento, key) in dateEvents">
                            <div class="flex">
                                <p class="dia-numero">{{key.split('/')[0]}}</p>
                                <p class="detalhe">{{meses[parseInt(key.split('/')[1]) - 1]}}/{{key.split('/')[2]}} - {{getDiaDaSemana(diaEvento)}}</p>     
                            </div>
                            <ul class="eventos" v-for="(evento) in diaEvento">
                                <li>
                                    <p class="from-programacao-view" @click="$root.openModalEvents(evento.id)">{{evento.title != 'Personalizado' ? evento.title + ' - ' : '' }} {{evento.descricao}}</p>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>
            </router-linkrticle>`,
    data(){
        return {
             ...getCalendarData(),
             dataSelected: '2023-08-01',
             modelo: 'mes-active',
             quantidadeDias: 42,
             calendarioAno: (new Date()).getFullYear()
         };
    },
    methods: Object.assign({}, getCalendarMethods(), {
        hoje: function(){
            this.dataCalendario = new Date();
            this.calendarioAno = (new Date()).getFullYear()
            this.arrayDatas = getArrayDatasMes(this.getMes(), this.getAno(), this.quantidadeDias);
        },
        pass: function(){
            switch(this.modelo){
                case 'mes-active':
                    this.passaMes()
                    break
                case 'ano-active':
                    this.passaAno()
                    break
            }
        },
        back: function(){
            switch(this.modelo){
                case 'mes-active':
                    this.voltaMes()
                    break
                case 'ano-active':
                    this.voltaAno()
                    break
            }
        },
        passaAno: function(){
            this.calendarioAno++
        },
        voltaAno: function(){
            this.calendarioAno--
        },
        isMesView: function(){
            return this.modelo === 'mes-active'
        },
        isAnoView: function(){
            return this.modelo === 'ano-active'
        },
        isProgramacaoView: function(){
            return this.modelo === 'programacao-active'
        },
        getDiaDaSemana(date){
            let data = new Date(date[0]['data'])
            let diasDaSemana = ['Domingo', 'Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado'];
            return diasDaSemana[data.getDay()]
        }
    }),
    mounted(){
        let vue_self = this;
        if (vue_self.$root.isPortrait()){
            vue_self.modelo = 'programacao-active'
        }
    }
});

Vue.component('navbar', {
    template: `
    <div> 
        <nav class="sidebar">
            <header>
                <div class="image-text">
                    <div class="image">
                    </div>
                    <p class="marca">Instituto Federal</p>
                    <p class="submarca">Campus Farroupilha</p>
                </div>
            </header>

            <div class="menu-bar">
                <button class='bx bxs-x-circle close-button' @click="$root.closeMenu()"></button>
                <div class="menu">
                    <ul class="menu-links">
                        <li class="nav-link"   :class="{'selected' : this.$root.page == 'home'}">
                            <router-link to="/">
                                <i class='bx bx-home-alt icon' ></i>
                                <span class="text nav-text">Home</span>
                            </router-link>
                        </li>
                        <li class="nav-link" :class="{'selected' : this.$root.page == 'agenda'}">
                            <router-link to="/agenda">
                                <i class='bx bx-calendar icon'></i>
                                <span class="text nav-text">Agenda</span>
                            </router-link>
                        </li>
                        <li class="nav-link" :class="{'selected' : this.$root.page == 'servidores'}" v-if="this.$root.dados.tipo == 'funcionario'">
                            <router-link to="/servidores">
                                <i class='bx bx-user icon'></i>
                                <span class="text nav-text">Servidores</span>
                            </router-link>
                        </li>
                        <li class="nav-link" :class="{'selected' : this.$root.page == 'arquivos'}">
                            <router-link to="/arquivos">
                                <i class="fa-regular fa-folder icon" style="font-size: 0.9vw;"></i>
                                <span class="text nav-text">Arquivos</span>
                            </router-link>
                        </li>
                        <li class="nav-link" :class="{'selected' : this.$root.page == 'registros'}" v-if="this.$root.dados.tipo == 'funcionario'">
                            <router-link to="/registros">
                                <i class='bx bx-history icon'></i>
                                <span class="text nav-text">Registros</span>
                            </router-link>
                        </li>
                        <li class="nav-link" :class="{'selected' : this.$root.page == 'configuracoes'}">
                            <router-link to="/configuracoes">
                                <i class='bx bx-cog icon'></i>
                                <span class="text nav-text">Configurações</span>
                            </router-link>
                        </li>
                    </ul>
                </div>

                <div class="bottom-content" onclick="window.location.href = '/logout'">
                    <i class='bx bx-log-out'></i>
                    <span class="text nav-text">
                        <p>
                            Logout
                        </p>
                    </span>
                </div>
            </div>
        </nav>

        <nav class="navbar">
<!--            <div class="search-box">-->
<!--                <i class="fa-solid fa-magnifying-glass"></i>-->
<!--                <input type="text" placeholder="Pesquisar...">-->
<!--            </div>-->
            <button @click="$root.openMenu()" class='bx bx-menu-alt-left'></button>
            <div class="user">
                <p class="nome">{{ this.$root.getNameUser() }}</p>
                <!-- <div class="photo"></div>-->
                <div class="notifications" v-if="$root.dados.tipo == 'servidor'">
                    <i
                      :class="{
                        'bx bxs-bell-ring': $root.dados.tipo == 'servidor' && $root.dados.notifications.length > 0,
                        'bx bx-bell': $root.dados.tipo != 'servidor' || $root.dados.notifications.length === 0
                      }"
                      @click="$root.openCloseNotification()"
                    ></i>
                </div>
            </div>
        </nav>
    </div>
    `,
    props: {
        page: {
            default : 0,
            required: false,
        },
    },
});

Vue.component('file-icon', {
    template: `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" data-name="Layer 2" preserveAspectRatio="xMidYMid meet" version="1.0" viewBox="355.1 263.9 1299.9 1482.2" zoomAndPan="magnify" style="fill: rgb(0, 0, 0);" original_string_length="1057"><g id="__id1644_siwp0kja45"><path d="M1433,1746.07H577a221.92,221.92,0,0,1-221.92-221.92V485.85A221.92,221.92,0,0,1,577,263.93h646l432,475.1v785.12A221.92,221.92,0,0,1,1433,1746.07Z" style="fill: rgb(190, 215, 244);"/></g><g id="__id1645_siwp0kja45"><path d="M1329.38,739h325.53L1223,263.93V632.61A106.43,106.43,0,0,0,1329.38,739Z" style="fill: rgb(115, 179, 224);"/></g><g id="__id1646_siwp0kja45"><path d="M955.56,1496.72A221.48,221.48,0,0,1,799,1118.62L998.56,919a162.48,162.48,0,0,1,229.78,0c63.35,63.35,63.35,166.43,0,229.78l-196.61,196.61a101.9,101.9,0,0,1-144.12-144.11l90-90a40,40,0,0,1,56.57,56.57l-90,90a21.9,21.9,0,1,0,31,31l196.61-196.61a82.48,82.48,0,1,0-116.64-116.64L855.51,1175.19a141.49,141.49,0,0,0,200.1,200.09l102.57-102.57a40,40,0,1,1,56.56,56.57l-102.56,102.57A220.07,220.07,0,0,1,955.56,1496.72Z" style="fill: rgb(115, 179, 224);"/></g></svg>`
})


