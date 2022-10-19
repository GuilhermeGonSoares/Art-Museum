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

my_scope();