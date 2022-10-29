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

function setDataForm(form){
    sessionStorage.setItem("load", true)
    sessionStorage.setItem("name", form.name.value);
    sessionStorage.setItem("date", form.date.value);
    sessionStorage.setItem("summary", form.summary.value);
    sessionStorage.setItem("description", form.description.value);
    sessionStorage.setItem("church", form.church.value);
    const options = form.author.querySelectorAll('option')
    const authors = []
    for(op of options){
        if (op.selected){
            authors.push(op.value)
        }
    }
    sessionStorage.setItem("authors", authors);

}

function form_data() {
    const form = document.querySelector('.create_painting')
    if (form) {
        const link_author = document.querySelector('#create_author')
        const link_church = document.querySelector('#create_church')
        const link_engraving = document.querySelector('#create_engraving')
        
        link_author.addEventListener('click', function () {
            setDataForm(form);         
        });
        link_church.addEventListener('click', function () {
            setDataForm(form);
        });
        link_engraving.addEventListener('click', function () {
            setDataForm(form);
        });

    } 
}
function loadForm(){
    const form = document.querySelector('.create_painting')
    const options = form.author.querySelectorAll('option')
    if (sessionStorage.getItem("load")) {
        window.addEventListener('load', function(event) {
            event.preventDefault();
            form.name.value = sessionStorage.getItem("name");
            form.date.value = sessionStorage.getItem("date");
            form.summary.value = sessionStorage.getItem("summary");
            form.description.value = sessionStorage.getItem("description"); 
            form.church.value = sessionStorage.getItem("church");
            authors_id = sessionStorage.getItem("authors").split(',')
            for(op of options){
                if (authors_id.includes(op.value)){
                    console.log(op)
                    op.selected = true
                    op.style.background = "hsl(206,100%,52%)"
                } else {
                    op.selected = false
                }
            }       
        });
    }
}

function loadEngraving(){
    window.addEventListener('load', function(e){
        e.preventDefault();
        let imageColumn = document.querySelectorAll('#image_visibility');
        let coluna = document.createElement('td');
        coluna.style.background = 'rgb(247, 247, 247)';
        for (imagem of imageColumn){
            imagem.parentNode.insertBefore(coluna.cloneNode(), imagem)
        }
        });
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
                option[i].style.background = "hsl(206,100%,52%)";
                selected.value = authors_selected.join(', ');

            } else{
                option[i].style.background = "";
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
    const btn = document.getElementById('show_image');
    const imageColumn = document.querySelectorAll('#image_visibility');
    const tagI = document.createElement('i');
    tagI.className = "fas fa-eye-slash";
    btn.appendChild(tagI);
    
    const coluna = document.createElement('td');
    coluna.style.background = '#e0e0e0';
    btn.addEventListener('click', function(e) {
        e.preventDefault();
        for (imagem of imageColumn){
            const newColuna = coluna.cloneNode()
            if (imagem.style.display !== 'none'){
                imagem.style.display = 'none';
                imagem.parentNode.insertBefore(newColuna, imagem)
                tagI.className = "fas fa-eye-slash";
                
            } else {
                imagem.parentNode.removeChild(imagem.parentNode.firstElementChild)
                imagem.style.display = '';
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
function limparSelect(select_city) {
    const allOptions = select_city.querySelectorAll('option')
    if (allOptions.length > 1){
        for (let i = 1; i <= allOptions.length; i++){
            console.log(allOptions)
            select_city.options.remove(allOptions[i])
        }
    }
}


function createOptionsCidade(select_city, estado){
    let cidades = JSON.parse(document.getElementById('cities').value)[estado];
    const op = document.createElement('option');

    for (cid of cidades){
        optionCreate = op.cloneNode()
        optionCreate.value = cid
        optionCreate.textContent = cid
        select_city.appendChild(optionCreate)
    } 
}

function listaCidadesBrasil() {
    const select_church = document.getElementById('id_state');
    const select_city = document.getElementById('id_city');
    select_church.addEventListener('change', function(e){

        e.preventDefault();
        if(select_church.value !== ''){
            console.log("limpar select")
            limparSelect(select_city);
            let estado = select_church.selectedOptions[0].text;
            console.log("colocar options")
            createOptionsCidade(select_city, estado);
            select_city.style.visibility='visible'
            select_city.parentNode.style.visibility='visible'
        } else {
            select_city.style.visibility='hidden'
            select_city.parentNode.style.visibility='hidden'
        }
    });

}


my_scope();

const current_page = document.location.href
if (current_page.includes('user/dashboard')){
    sessionStorage.clear()
}

if (current_page.includes("user/painting/create") || (current_page.includes("user/painting") && current_page.includes("edit"))){
    loadForm();
    form_data();
    resetSession();
    desmarcarCampoSelectMultiple();
    
}

if (current_page.includes("user/engraving/all")){
    showHideTable();
    loadEngraving();
}

if (current_page.includes('church/create')){
    listaCidadesBrasil();
}