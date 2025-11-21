document.addEventListener('DOMContentLoaded', () => {

    /* --------------------------------------------------------------------
     * 1. DEFINICIÓN DE ELEMENTOS Y FORMULARIOS
     * -------------------------------------------------------------------- */
    // Formulario de Información
    const infoForm = document.getElementById('info-form');
    const editInfoButton = document.querySelector('.edit-info-btn');
    const usernameInput = document.getElementById('username');
    const fullNameInput = document.getElementById('full-name');
    const emailInput = document.getElementById('email');

    // Elementos de Error para Información
    const usernameError = document.getElementById('username-error');
    const fullNameError = document.getElementById('full-name-error');
    const emailError = document.getElementById('email-error');
    
    // Formulario de Contraseña
    const passwordForm = document.getElementById('password-form');
    const messageDisplay = document.getElementById('message');
    const currentPassInput = document.getElementById('current-password');
    const newPassInput = document.getElementById('new-password');
    const confirmPassInput = document.getElementById('confirm-password');

    // Elementos de Foto/Modal
    const editPhotoBtn = document.querySelector('.edit-btn');
    const profileInput = document.getElementById('profile-input');
    const profileImage = document.getElementById('profile-image');
    const savePhotoBtn = document.querySelector('.save-photo-btn');

    // Toggle for password visibility buttons
    const togglePassButtons = document.querySelectorAll('.toggle-pass');
    togglePassButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetId = btn.dataset.target;
            if (!targetId) return;
            const input = document.getElementById(targetId);
            if (!input) return;
            if (input.type === 'password') {
                input.type = 'text';
                btn.textContent = '🙈';
                btn.setAttribute('aria-pressed', 'true');
            } else {
                input.type = 'password';
                btn.textContent = '👁️';
                btn.setAttribute('aria-pressed', 'false');
            }
        });
    });


    /* --------------------------------------------------------------------
     * 2. FUNCIONES DE VALIDACIÓN
     * -------------------------------------------------------------------- */

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
            return { valid: false, msg: 'Error: Debes ingresar nombre(s) y apellido(s).' };
        }
        const regex = /^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$/; 
        if (fullName.length > 35) {
            return { valid: false, msg: 'Máximo 35 caracteres.' };
        }
        if (!regex.test(fullName)) {
            return { valid: false, msg: 'Error: Solo letras y espacios. No se permiten números.' };
        }
        return { valid: true };
    }

    function validateEmail(email) {
        // Validación de formato de email estándar
        const generalRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/; 
        if (!generalRegex.test(email)) {
            return { valid: false, msg: 'Error: Formato de email inválido.' };
        }
        return { valid: true };
    }

    function validatePassword(password) {
        // Requisitos: 8 a 20 caracteres. Acepta letras, números, puntos, guiones bajos y guiones
        const regex = /^[a-zA-Z0-9._-]{8,20}$/; 
        if (!regex.test(password)) {
            return {
                valid: false,
                msg: 'Contraseña debe ser de 8-20 caracteres. Solo letras, números, ., _ y -'
            };
        }
        return { valid: true };
    }


    /* --------------------------------------------------------------------
     * 3. FUNCIONES DE UTILIDAD (Mensajes/Errores)
     * -------------------------------------------------------------------- */
     
    function showMessage(msg, type) {
        messageDisplay.textContent = msg;
        messageDisplay.classList.remove("hidden");
        messageDisplay.style.padding = "10px"; // Añadir padding si es necesario
        messageDisplay.style.borderRadius = "4px";

        if (type === "success") {
            messageDisplay.style.background = "#d4edda"; 
            messageDisplay.style.color = "#155724"; 
        } else {
            messageDisplay.style.background = "#f8d7da"; 
            messageDisplay.style.color = "#721c24"; 
        }
        
        setTimeout(() => {
            messageDisplay.classList.add("hidden");
        }, 5000);
    }

    function displayError(errorElement, msg, inputElement) {
        hideAllErrors(); 
        
        errorElement.textContent = msg;
        errorElement.classList.remove('hidden');
        inputElement.style.borderColor = "#dc3545"; // Rojo
        inputElement.focus();
        
        showMessage("Por favor, corrige los errores en el formulario.", "error");
    }
    
    function hideAllErrors() {
        // Ocultar mensajes de error de los campos de info
        [usernameError, fullNameError, emailError].forEach(el => el.classList.add('hidden'));
        
        // Restaurar bordes (usando el gris medio de tu CSS)
        [usernameInput, fullNameInput, emailInput].forEach(el => el.style.borderColor = "#ced4da");
        
        // Ocultar mensaje general
        messageDisplay.classList.add("hidden");
    }


    /* --------------------------------------------------------------------
     * 4. ✏️ LÓGICA DE EDICIÓN / GUARDADO DE INFORMACIÓN
     * -------------------------------------------------------------------- */
    editInfoButton.addEventListener('click', () => {
        const isReadonly = usernameInput.readOnly;

        if (isReadonly) {
            // MODO EDICIÓN: Habilitar campos
            usernameInput.readOnly = false;
            fullNameInput.readOnly = false;
            emailInput.readOnly = false;

            usernameInput.style.background = "#fff";
            fullNameInput.style.background = "#fff";
            emailInput.style.background = "#fff";

            editInfoButton.textContent = "Guardar Información";
            hideAllErrors();
        } else {
            // MODO GUARDAR: Validar y enviar al servidor
            
            // 1. Validar en el cliente
            const u = validateUsername(usernameInput.value);
            const f = validateFullName(fullNameInput.value);
            const e = validateEmail(emailInput.value);

            // Si hay errores, mostrarlos y detener el proceso
            if (!u.valid) return displayError(usernameError, u.msg, usernameInput);
            if (!f.valid) return displayError(fullNameError, f.msg, fullNameInput);
            if (!e.valid) return displayError(emailError, e.msg, emailInput);

            // 2. Si la validación es exitosa, disparamos el envío POST a Django.
            // La recarga, el mensaje de éxito y la readOnly se manejarán en la vista.
            infoForm.submit(); 
            
            // Opcional: Deshabilitar el botón temporalmente para evitar doble clic
            editInfoButton.disabled = true;
        }
    });


    /* --------------------------------------------------------------------
     * 5. 🔐 LÓGICA DE CAMBIO DE CONTRASEÑA
     * -------------------------------------------------------------------- */
    passwordForm.addEventListener('submit', (e) => {
        e.preventDefault(); // Detener el envío local para validar

        const current = currentPassInput.value;
        const newPass = newPassInput.value;
        const confirm = confirmPassInput.value;

        if (!current || !newPass || !confirm)
            return showMessage("Error: Todos los campos son obligatorios.", "error");

        const valid = validatePassword(newPass);
        if (!valid.valid) return showMessage("Error: " + valid.msg, "error");

        if (newPass !== confirm)
            return showMessage("Error: Las contraseñas no coinciden.", "error");
        
        // Si la validación en JS es correcta, se permite el envío a Django (POST).
        passwordForm.submit();
        
        // Opcional: Deshabilitar el botón
        passwordForm.querySelector('.change-password-btn').disabled = true;
    });


    /* --------------------------------------------------------------------
     * 6. 🖼️ LÓGICA DE FOTO DE PERFIL Y RECORTE (CROPPING)
     * -------------------------------------------------------------------- */
    let uploadedImage = null;
    let cropCanvas = null;
    let ctx = null;
    let selection = { x: 0, y: 0, w: 0, h: 0 };
    const CANVAS_SIZE = 400;

    function createCropModal() {
        // ... (Tu código para crear el modal dinámicamente) ...
        // [Este bloque es largo y está bien, lo omito aquí por brevedad, pero mantenlo intacto en tu archivo]
        
        // --- INICIO DE TU CÓDIGO DE MODAL ---
        const modal = document.createElement("div");
        modal.className = "crop-modal";
        modal.id = "cropper-modal-instance";
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
        
        cropCanvas.width = CANVAS_SIZE;
        cropCanvas.height = CANVAS_SIZE;

        ctx.drawImage(uploadedImage, 0, 0, CANVAS_SIZE, CANVAS_SIZE);

        setupCropEvents(modal);
        // --- FIN DE TU CÓDIGO DE MODAL ---
    }

    function setupCropEvents(modal) {
        let isDrawing = false;
        let startX, startY;

        function draw() {
            ctx.clearRect(0, 0, CANVAS_SIZE, CANVAS_SIZE);
            ctx.drawImage(uploadedImage, 0, 0, CANVAS_SIZE, CANVAS_SIZE);

            if (selection.w > 0 && selection.h > 0) {
                ctx.strokeStyle = "#27ae60";
                ctx.lineWidth = 3;
                ctx.strokeRect(selection.x, selection.y, selection.w, selection.h);
                
                ctx.fillStyle = "rgba(0, 0, 0, 0.5)";
                
                ctx.fillRect(0, 0, CANVAS_SIZE, selection.y);
                ctx.fillRect(0, selection.y, selection.x, selection.h);
                ctx.fillRect(selection.x + selection.w, selection.y, CANVAS_SIZE - (selection.x + selection.w), selection.h);
                ctx.fillRect(0, selection.y + selection.h, CANVAS_SIZE, CANVAS_SIZE - (selection.y + selection.h));
            }
        }
        
        function getCoords(e) {
            const rect = cropCanvas.getBoundingClientRect();
            return {
                x: e.clientX - rect.left,
                y: e.clientY - rect.top
            };
        }

        cropCanvas.onmousedown = (e) => {
            isDrawing = true;
            const coords = getCoords(e);
            startX = coords.x;
            startY = coords.y;
            selection = { x: startX, y: startY, w: 0, h: 0 };
        };

        cropCanvas.onmousemove = (e) => {
            if (!isDrawing) return;

            const coords = getCoords(e);
            const w = coords.x - startX;
            const h = coords.y - startY;

            selection.x = Math.min(startX, coords.x);
            selection.y = Math.min(startY, coords.y);
            selection.w = Math.abs(w);
            selection.h = Math.abs(h);
            
            draw();
        };

        cropCanvas.onmouseup = () => {
            isDrawing = false;
            // Forzar selección cuadrada
            if (selection.w > selection.h) {
                selection.h = selection.w;
            } else {
                selection.w = selection.h;
            }
            draw();
        };

        document.getElementById("cancel-crop").onclick = () => modal.remove();

        document.getElementById("apply-crop").onclick = () => {
            if (selection.w < 10 || selection.h < 10) { 
                alert("Debes seleccionar un área válida.");
                return;
            }

            // Crear un canvas temporal para el recorte final (200x200)
            const finalCanvas = document.createElement("canvas");
            finalCanvas.width = 200;
            finalCanvas.height = 200;
            const finalCtx = finalCanvas.getContext("2d");

            // Calcular los factores de escala
            const scaleX = uploadedImage.width / CANVAS_SIZE;
            const scaleY = uploadedImage.height / CANVAS_SIZE;

            // Dibujar la parte seleccionada de la imagen original
            finalCtx.drawImage(
                uploadedImage,
                selection.x * scaleX, 
                selection.y * scaleY, 
                selection.w * scaleX, 
                selection.h * scaleY, 
                0, 0, 
                200, 200 
            );

            // 🚨 IMPORTANTE: Subir la imagen recortada al servidor (PENDIENTE)
            // Ya que estás enviando el formulario info-form, necesitarías convertir este canvas
            // en un objeto File y adjuntarlo a un FormData para enviarlo junto con el resto
            // de los datos de edición, o enviarlo por separado con Fetch API.
            
            // Convertir el canvas final a Blob y adjuntarlo al input file oculto
            finalCanvas.toBlob((blob) => {
                if (!blob) {
                    // Fallback: usar dataURL si no se pudo crear el blob
                    profileImage.src = finalCanvas.toDataURL("image/png");
                    modal.remove();
                    return;
                }

                // Crear un File a partir del Blob
                const file = new File([blob], 'profile.png', { type: 'image/png' });

                // Usar DataTransfer para asignarlo a profileInput.files
                try {
                    const dataTransfer = new DataTransfer();
                    dataTransfer.items.add(file);
                    profileInput.files = dataTransfer.files;
                } catch (e) {
                    // Algunos navegadores antiguos podrían no soportar DataTransfer constructor
                    console.warn('No se pudo asignar el archivo al input programáticamente:', e);
                }

                // Mostrar vista previa usando un object URL (más eficiente que dataURL)
                try {
                    const objectUrl = URL.createObjectURL(file);
                    profileImage.src = objectUrl;
                } catch (e) {
                    profileImage.src = finalCanvas.toDataURL("image/png");
                }

                modal.remove();
            }, 'image/png');
        };
    }


    /* --------------------------------------------------------------------
     * 📸 EVENTOS DE FOTO
     * -------------------------------------------------------------------- */
    editPhotoBtn.addEventListener("click", () => {
        profileInput.click();
    });

    if (savePhotoBtn) {
        savePhotoBtn.addEventListener('click', async () => {
            // Upload the info form (including profile picture) via fetch + FormData.
            if (!infoForm) return;

            // Get CSRF token from hidden input rendered by Django
            const csrfInput = infoForm.querySelector('input[name="csrfmiddlewaretoken"]');
            const csrfToken = csrfInput ? csrfInput.value : null;

            const formData = new FormData(infoForm);

            // Ensure the server receives the correct form_type
            if (!formData.has('form_type')) formData.set('form_type', 'profile_update');

            // Disable button to avoid double submits
            savePhotoBtn.disabled = true;
            savePhotoBtn.textContent = 'Guardando...';

            try {
                const resp = await fetch(infoForm.action, {
                    method: 'POST',
                    headers: csrfToken ? { 'X-CSRFToken': csrfToken } : {},
                    body: formData,
                    credentials: 'same-origin',
                });

                // If the server redirected, follow it; otherwise reload to show changes
                if (resp.redirected) {
                    window.location.href = resp.url;
                } else {
                    // Try to reload to reflect the saved image
                    window.location.reload();
                }
            } catch (err) {
                console.error('Error uploading profile image:', err);
                alert('Ocurrió un error subiendo la imagen. Revisa la consola.');
                savePhotoBtn.disabled = false;
                savePhotoBtn.textContent = 'Guardar Cambios';
            }
        });
    }

    profileInput.addEventListener("change", (event) => {
        const file = event.target.files[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = () => {
            uploadedImage = new Image();
            uploadedImage.onload = () => {
                document.getElementById("cropper-modal-instance")?.remove();
                createCropModal();
            };
            uploadedImage.src = reader.result;
        };
        reader.readAsDataURL(file);
    });

});