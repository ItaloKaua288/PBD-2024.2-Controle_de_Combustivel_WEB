document.querySelector('#alterar-senha-btn').addEventListener('click', ()=>{
    let password_box = document.getElementById('password-box')
    let password_box_btn = document.getElementById('password-btns')
    const campos = '<label for="new-password" class="form-label">Nova Senha:<input class="form-control" minlength="4" maxlength="12" type="text" name="new-password" id="new-password"></label><label for="confirm-password" class="form-label">Confirmar Senha: <input class="form-control" type="text" name="confirm-password"  minlength="4" maxlength="12" id="confirm-password"></label>'
    const input_btn = '<input type="submit" value="Confirmar" class="btn btn-primary">'
    console.log(password_box_btn);
    
    if (password_box.innerHTML != campos)
        password_box.innerHTML = campos
    if (!password_box_btn.innerHTML.includes(input_btn))
        password_box_btn.innerHTML += input_btn
})