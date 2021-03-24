let folderSelected = '';
let vaultSelected = '';

const revealEncryptionPopUp = async () => {
    const folderName = document.getElementById("vault_name");
    const folderError = document.getElementById('folder_name_error');

    if(folderName.value == "") {
        folderError.classList = "text-sm text-red-500 font-bold ml-1 mb-1";
        return;
    }
    folderError.classList = "text-sm text-red-500 font-bold ml-1 mb-1 hidden";

    const folderFound = await eel.name_vault_search(folderName.value)()
    if (!folderFound) {
        folderError.classList = "text-sm text-red-500 font-bold ml-1 mb-1";
        return;
    }
    folderSelected = folderName.value;
    document.getElementById("encypt_folder_pass").classList = "mt-5";
    document.getElementById("encrypt_password_folder").innerText = `Encrypt: ${folderName.value}/`;
}

const decryptVaultFile = async () => {
    const password = document.getElementById("decrypt_password").value;
    const passwordError = document.getElementById("decrypt_password_error");
    if (password == "") {
        passwordError.classList = "text-sm text-red-500 font-bold ml-1 mb-1";
        return;
    }

    const correctPassword = await eel.decrypt_folder(vaultSelected, password)();
    if (!correctPassword) {
        passwordError.classList = "text-sm text-red-500 font-bold ml-1 mb-1";
        return;
    }
    passwordError.classList = "text-sm text-red-500 font-bold ml-1 mb-1 hidden";
    closeDecryptFolderPopUp();
}

const encryptVaultFolder = async () => {
    const password = document.getElementById("encrypt_password").value;
    const passwordVerify = document.getElementById("encrypt_password_verify").value;
    const passwordError = document.getElementById("encrypt_password_error");
    if (password == "" || password !== passwordVerify) {
        passwordError.classList = "text-sm text-red-500 font-bold ml-1 mb-1";
        return;
    }
    await eel.encrypt_folder(folderSelected, password)();
    closeEcryptFolderPopUp();
}

const revealDecryptionPopUp = (vaultName) => {
    vaultSelected = vaultName
    document.getElementById("decrypt_vault_pass").classList = "mt-5";
    document.getElementById("decrypt_password_vault").innerText = `Decrypt: ${vaultName}`;
}

const closeEcryptFolderPopUp = () => {
    document.getElementById("encypt_folder_pass").classList = "mt-5 hidden";
}

const closeDecryptFolderPopUp = () => {
    document.getElementById("decrypt_vault_pass").classList = "mt-5 hidden";
}