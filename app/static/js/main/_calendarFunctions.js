const getArrayDatasMes = (mes, ano, dias_mes = 42) => {
    let array = [];
    let indexPrimeiroDia = new Date(ano, mes, 1).getDay();
    for (let i = 0; i < dias_mes; i++) {
        array[i] = new Date(ano, mes, i - indexPrimeiroDia + 1);
    }
    return array;
};
const getArrayDatasAno = (ano) => {
    let array = [];
    for(mes = 0; mes < 12; mes++){
        array.push(getArrayDatasMes(mes, ano, 35))
    }
    return array;
};

const getCalendarData = () => {
    return {
      meses: [
        'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto',
        'Setembro', 'Outubro', 'Novembro', 'Dezembro'
      ],
      dataCalendario: new Date(),
      dataAtual: new Date(),
      dataSelected: '',
      arrayDatas: [],
      quantidadeDias: 42
    };
};

const getCalendarMethods = () => {
    return {
        passaMes() {
            this.dataCalendario.setMonth(this.dataCalendario.getMonth() + 1);
            this.arrayDatas = getArrayDatasMes(this.getMes(), this.getAno(), this.quantidadeDias);
        },
        voltaMes() {
            this.dataCalendario.setMonth(this.dataCalendario.getMonth() - 1);
            this.arrayDatas = getArrayDatasMes(this.getMes(), this.getAno(), this.quantidadeDias);
        },
        getMes() {
            return this.dataCalendario.getMonth();
        },
        getAno() {
            return this.dataCalendario.getFullYear();
        },
        getDataFormatada(data = this.dataAtual) {
            const ano = data.getFullYear();
            const mes = String(data.getMonth() + 1).padStart(2, '0');
            const dia = String(data.getDate()).padStart(2, '0');
            return `${ano}-${mes}-${dia}`;
        },
        selectData(index) {
            this.dataSelected = this.getDataFormatada(this.arrayDatas[index]);
        },
        isDataAtual(data) {
            return this.getDataFormatada(data) === this.getDataFormatada(this.dataAtual);
        },
        isSelected(data) {
            return this.getDataFormatada(data) === this.dataSelected;
        },
    }
};



const calendarBase = {
    template: `
    <div class="calendar">
        <div class="head">
            <div class="mes-ano">
                <p class="mes">{{ meses[getMes()] }}</p>
                <p class="ano">{{ getAno() }}</p>
            </div>
            <div class="arrows">
                <button @click="voltaMes()"><</button>
                <button @click="passaMes()">></button>
            </div>
        </div>
        <div class="datas">
            <div class="header">
                <div class="dia">
                    <p>Dom</p>
                </div>
                <div class="dia">
                    <p>Seg</p>
                </div>
                <div class="dia">
                    <p>Ter</p>
                </div>
                <div class="dia">
                    <p>Qua</p>
                </div>
                <div class="dia">
                    <p>Qui</p>
                </div>
                <div class="dia">
                    <p>Sex</p>
                </div>
                <div class="dia">
                    <p>Sáb</p>
                </div>
            </div>
            <div class="dias">
                <div
                    class="dia"
                    v-for="(item, key) in arrayDatas"
                    :class="{'gray' : item.getMonth() !== getMes(), 'hoje': isDataAtual(item), 'selected': isSelected(item)}"
                    @click="selectData(key)"
                    :key="key"
                >
                    <p>
                        {{ item.getDate() }}
                    </p>
                </div>
            </div>
        </div>
    </div>
    `,
    data() {
        return getCalendarData();
    },
    mounted() {
        this.arrayDatas = getArrayDatasMes(this.getMes(), this.getAno(), this.quantidadeDias);
    },
    methods: getCalendarMethods()
}