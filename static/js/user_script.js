console.log("¿Cargó el JS?");


document.addEventListener('DOMContentLoaded', () => {

    /* --------------------------------------------------------------------
       ELEMENTOS PRINCIPALES
    -------------------------------------------------------------------- */
    const editPhotoBtn = document.querySelector('.edit-btn');
    const profileImage = document.getElementById('profile-image');

    const editInfoButton = document.querySelector('.edit-info-btn');
    const usernameInput = document.getElementById('username');
    const fullNameInput = document.getElementById('full-name');
    const emailInput = document.getElementById('email');

    const passwordForm = document.getElementById('password-form');
    const message = document.getElementById('message');


    /* --------------------------------------------------------------------
       💠 MODAL PARA CARGAR Y RECORTAR IMAGEN
    -------------------------------------------------------------------- */
    let modal, cropCanvas, ctx, uploadedImage, selection = null;

    function createCropModal() {
        modal = document.createElement("div");
        modal.className = "crop-modal";
        modal.innerHTML = `
            <div class="crop-content">
                <h3>Recortar Imagen</h3>
                <canvas id="crop-canvas"></canvas>

                <div class="crop-buttons">
                    <button id="cancel-crop" class="cancel-btn">Cancelar</button>
                    <button id="apply-crop" class="apply-btn">Aplicar</button>
                </div>
            </div>
        `;
        document.body.appendChild(modal);

        cropCanvas = document.getElementById("crop-canvas");
        ctx = cropCanvas.getContext("2d");

        setupCropEvents();
    }

    function setupCropEvents() {
        let isDrawing = false;
        let startX, startY;

        cropCanvas.onmousedown = (e) => {
            isDrawing = true;
            startX = e.offsetX;
            startY = e.offsetY;
        };

        cropCanvas.onmousemove = (e) => {
            if (!isDrawing) return;

            const x = e.offsetX;
            const y = e.offsetY;

            ctx.clearRect(0, 0, cropCanvas.width, cropCanvas.height);
            ctx.drawImage(uploadedImage, 0, 0, cropCanvas.width, cropCanvas.height);

            ctx.strokeStyle = "#27ae60";
            ctx.lineWidth = 2;
            ctx.strokeRect(startX, startY, x - startX, y - startY);

            selection = { x: startX, y: startY, w: x - startX, h: y - startY };
        };

        cropCanvas.onmouseup = () => {
            isDrawing = false;
        };

        document.getElementById("cancel-crop").onclick = () => modal.remove();

        document.getElementById("apply-crop").onclick = () => {
            if (!selection) return;

            const temp = document.createElement("canvas");
            temp.width = 200;
            temp.height = 200;

            const tctx = temp.getContext("2d");

            tctx.drawImage(
                uploadedImage,
                selection.x * (uploadedImage.width / cropCanvas.width),
                selection.y * (uploadedImage.height / cropCanvas.height),
                selection.w * (uploadedImage.width / cropCanvas.width),
                selection.h * (uploadedImage.height / cropCanvas.height),
                0, 0,
                200, 200
            );

            profileImage.src = temp.toDataURL("image/png");
            modal.remove();
        };
    }


    /* --------------------------------------------------------------------
       📸 ABRIR SELECTOR DE ARCHIVOS
    -------------------------------------------------------------------- */
    editPhotoBtn.addEventListener("click", () => {
        const input = document.createElement("input");
        input.type = "file";
        input.accept = "image/*";

        input.onchange = (event) => {
            const file = event.target.files[0];
            if (!file) return;

            const reader = new FileReader();
            reader.onload = () => {
                uploadedImage = new Image();
                uploadedImage.onload = () => {
                    createCropModal();

                    cropCanvas.width = 400;
                    cropCanvas.height = 400;

                    ctx.drawImage(uploadedImage, 0, 0, 400, 400);
                };
                uploadedImage.src = reader.result;
            };
            reader.readAsDataURL(file);
        };

        input.click();
    });


    /* --------------------------------------------------------------------
       📌 VALIDACIONES (LAS MISMAS QUE ME DISTE)
    -------------------------------------------------------------------- */

    function validateUsername(username) {
        if (username.trim().length === 0) {
            return { valid: false, msg: 'Error: El Nombre de Usuario no puede estar vacío.' };
        }
        const regex = /^[a-zA-Z0-9._-]+$/;
        if (username.length > 30) {
            return { valid: false, msg: 'Error: Máximo 30 caracteres.' };
        }
        if (!regex.test(username)) {
            return { valid: false, msg: 'Error: Solo letras, números, ., _ y -' };
        }
        return { valid: true };
    }

    function validateFullName(fullName) {
        if (fullName.trim().length === 0) {
            return { valid: false, msg: 'Error: Debes ingresar nombre.' };
        }
        const regex = /^[a-zA-Z\s]+$/;
        if (fullName.length > 35) {
            return { valid: false, msg: 'Máximo 35 caracteres.' };
        }
        if (!regex.test(fullName)) {
            return { valid: false, msg: 'Solo letras y espacios.' };
        }
        return { valid: true };
    }

    function validateEmail(email) {
        const strictRegex = /^([a-zA-Z0-9._-]{1,23})@([a-zA-Z0-9.-]{9})\.([a-zA-Z]{6})$/;
        if (!strictRegex.test(email)) {
            return { valid: false, msg: 'Formato de email inválido.' };
        }
        return { valid: true };
    }

    function validatePassword(password) {
        const regex = /^[a-zA-Z0-9._-]{8,20}$/;
        if (!regex.test(password)) {
            return {
                valid: false,
                msg: 'Contraseña 8-20 chars. Solo letras, números, ., _ y -'
            };
        }
        return { valid: true };
    }


    /* --------------------------------------------------------------------
       ✏️ EDITAR / GUARDAR INFORMACIÓN
    -------------------------------------------------------------------- */
    editInfoButton.addEventListener('click', () => {
        const isReadonly = usernameInput.readOnly;

        if (isReadonly) {
            usernameInput.readOnly = false;
            fullNameInput.readOnly = false;
            emailInput.readOnly = false;

            usernameInput.style.background = "#fff";
            fullNameInput.style.background = "#fff";
            emailInput.style.background = "#fff";

            editInfoButton.textContent = "Guardar Información";
        } else {
            const u = validateUsername(usernameInput.value);
            const f = validateFullName(fullNameInput.value);
            const e = validateEmail(emailInput.value);

            if (!u.valid) return showMessage(u.msg, 'error');
            if (!f.valid) return showMessage(f.msg, 'error');
            if (!e.valid) return showMessage(e.msg, 'error');

            usernameInput.readOnly = true;
            fullNameInput.readOnly = true;
            emailInput.readOnly = true;

            usernameInput.style.background = "#eee";
            fullNameInput.style.background = "#eee";
            emailInput.style.background = "#eee";

            editInfoButton.textContent = "Editar Información";

            showMessage("Información guardada correctamente.", "success");
        }
    });


    /* --------------------------------------------------------------------
       🔐 CAMBIO DE CONTRASEÑA
    -------------------------------------------------------------------- */
    passwordForm.addEventListener('submit', (e) => {
        e.preventDefault();

        const current = document.getElementById('current-password').value;
        const newPass = document.getElementById('new-password').value;
        const confirm = document.getElementById('confirm-password').value;

        if (!current || !newPass || !confirm)
            return showMessage("Todos los campos son obligatorios.", "error");

        const valid = validatePassword(newPass);
        if (!valid.valid) return showMessage(valid.msg, "error");

        if (newPass !== confirm)
            return showMessage("Las contraseñas no coinciden.", "error");

        showMessage("¡Contraseña cambiada con éxito!", "success");
        passwordForm.reset();
    });


    /* --------------------------------------------------------------------
       🟩 FUNCION PARA MENSAJES
    -------------------------------------------------------------------- */
    function showMessage(msg, type) {
        message.textContent = msg;
        message.classList.remove("hidden");

        message.style.background = type === "success" ? "#d4edda" : "#f8d7da";
        message.style.color = type === "success" ? "#155724" : "#721c24";
    }
});
