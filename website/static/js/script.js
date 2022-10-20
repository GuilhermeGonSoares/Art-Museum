function my_scope() {
    const forms = document.querySelectorAll('.form-delete');
    for (const form of forms){
        form.addEventListener('submit', function (event) {
            event.preventDefault();
            const confirmed = confirm("Deseja excluir esse post?");
            if (confirmed) {
                form.submit();
            }
        });
    }
}

function form_data() {
    const form = document.querySelector('.create_painting')
    if (form) {
        let link_author = document.querySelector('#create_author')
        let link_church = document.querySelector('#create_church')
        link_author.addEventListener('click', function () {
            sessionStorage.setItem("name", form.name.value);
            sessionStorage.setItem("date", form.date.value);
            sessionStorage.setItem("summary", form.summary.value);
            sessionStorage.setItem("description", form.description.value);
        });
        link_church.addEventListener('click', function () {
            sessionStorage.setItem("name", form.name.value);
            sessionStorage.setItem("date", form.date.value);
            sessionStorage.setItem("summary", form.summary.value);
            sessionStorage.setItem("description", form.description.value);
        });

    } 
}
function loadForm(){
    const form = document.querySelector('.create_painting')
    if (form) {
        window.addEventListener('load', function(event) {
            event.preventDefault();
            form.name.value = sessionStorage.getItem("name");
            form.date.value = sessionStorage.getItem("date");
            form.summary.value = sessionStorage.getItem("summary");
            form.description.value = sessionStorage.getItem("description"); 
        });
    }
}
function resetSession() {
    const form = document.querySelector('.create_painting')
    form.addEventListener("submit", function(event){
        event.preventDefault();
        sessionStorage.clear();
        form.submit();
    })
}
function resetSessionDashboard() {
    const link = document.querySelector('#dashboard-button')
    link.addEventListener("click", function(event){   
        sessionStorage.clear();
    })
}

my_scope();

const current_page = document.location.href
if (current_page.includes("painting/create")){
    loadForm();
    form_data();
    resetSession();
}

if (current_page === "http://localhost:8081/user/dashboard/"){
    resetSessionDashboard();
}