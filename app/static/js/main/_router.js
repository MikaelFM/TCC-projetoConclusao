var html = {
    'home': "",
    'agenda': "",
    'servidores': "",
    'arquivos': "",
    'registros': "",
    'configuracoes': ""
};

var router;

async function fetchHTML() {
    try {
        const response = await $.ajax({
            url: '/getHTML',
            type: 'GET'
        });
        html = response;
        initializeVueRouter();
        AppCreate();
    } catch (error) {
        console.log('Ocorreu um erro: ', error);
    }
}

function initializeVueRouter() {
    const errorNotFound = {
        template: '<div class="content not-found">Erro 404</div>'
    };

    const routes = Object.keys(html).map(key => ({
        path: key == "home" ? '/' : `/${key}`,
        component: {
            template: html[key] || errorNotFound.template,
            mounted() {
                this.$root.page = key;
            }
        }
    }));

    router = new VueRouter({ routes });
}

fetchHTML();