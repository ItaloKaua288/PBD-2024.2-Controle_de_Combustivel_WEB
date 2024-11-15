document.querySelector('#alterar-senha-btn').addEventListener('click', ()=>{
    let password_box = document.getElementById('password-box')
    const campos = '<label for="new-password" class="form-label">Nova Senha:<input class="form-control" minlength="4" maxlength="12" type="text" name="new-password" id="new-password"></label><label for="confirm-password" class="form-label">Confirmar Senha: <input class="form-control" type="text" name="confirm-password"  minlength="4" maxlength="12" id="confirm-password"></label>'
    if (password_box.innerHTML != campos)
        password_box.innerHTML = campos
})