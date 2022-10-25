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

function confirmCancel() {
    addEventListener('click', function (event) {
        const confirmed = confirm("Deseja cancelar?")
        if (confirmed) {
            history.back();
        }
    })
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
    const link = document.querySelector('.dashboard-button')
    link.addEventListener("click", function(event){   
        sessionStorage.clear();
    })
}

function searchInFormPaintings(input_id, select_id){
    let input, filter, select, option, i, txtValue;
    input = document.getElementById(input_id);
    filter = input.value.toUpperCase();
    select = document.getElementById(select_id);
    option = select.getElementsByTagName('option');

    for (i = 0; i < option.length; i++){
        txtValue = option[i].textContent || option[i].innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1){
            option[i].style.display = "";
        } else {
            option[i].style.display = "none";
        }
    }
}



function desmarcarCampoSelectMultiple() {
    let select = document.getElementById('id_author');
    let option = select.getElementsByTagName('option');
    let selected = document.getElementById('author_selected');
    const authors_selected = [];
    for(let i = 0; i < option.length; i++){
        option[i].addEventListener('mousedown', function(event){
            if (!option[i].selected){
                authors_selected.push(option[i].textContent);
                selected.value = authors_selected.join();

            } else{
                let pos = authors_selected.indexOf(option[i].textContent);
                if(pos > -1){
                    authors_selected.splice(pos,1);
                }
                selected.value = authors_selected.join();
            }
            
            option[i].selected = !option[i].selected;
            
            event.preventDefault();
        })
    }
    
}

function showHideTable() {
    let btn = document.getElementById('show_image')
    let imageColumn = document.querySelectorAll('#image_visibility')
    let tagI = document.createElement('i')
    tagI.className = "fas fa-eye-slash";
    btn.appendChild(tagI);
    
    btn.addEventListener('click', function(e) {
        e.preventDefault();
        for (imagem of imageColumn){
            if (imagem.style.visibility === 'visible'){
                imagem.style.visibility = ' ';
                tagI.className = "fas fa-eye-slash";
                
            } else {
                imagem.style.visibility = 'visible';
                tagI.className = "fas fa-eye";
                btn.text
            }
        }
    })
}

function searchElementTable() {
    let input, filter, line, name_engraving, i, txtValue;
    input = document.getElementById('search_engraving');
    filter = input.value.toUpperCase();
    line = document.querySelectorAll('#linha_tabela')

    for (i = 0; i < line.length; i++){
        name_engraving = line[i].getElementsByClassName('main-table-name')[0]
        
        txtValue = name_engraving.textContent || name_engraving.innerText;
        
        if (txtValue.toUpperCase().indexOf(filter) > -1){
            line[i].style.display = "";
        } else {
            line[i].style.display = "none";
        }
    }
}


my_scope();

const current_page = document.location.href
if (current_page.includes("painting/create")){
    loadForm();
    form_data();
    resetSession();
    
}
if (current_page.includes("user/painting")){
    desmarcarCampoSelectMultiple();
}

if (current_page.includes("user/engraving/all")){
    showHideTable();
}
