async function getVaultFiles() {
    const vaultFiles = await eel.sub_vault_search()();
    const table = document.getElementById('vault_table_body');

    table.innerHTML = '';
    if(vaultFiles == null) {
        table.innerHTML = `<tr>
                            <td class="w-1/2 pb-3 pt-3 font-bold">-</td>
                            <td class="w-1/4 pb-3 pt-3 text-center">-</td>
                            <td class="w-1/4 pb-3 pt-3 text-center">-</td>
                            </tr>`
        return;
    }

    vaultFiles.forEach(file => {
        table.innerHTML += `<tr style="border-bottom: 3px solid red;">
                            <td class="w-1/2 pb-3 pt-3 font-bold">${file[0]}</td>
                            <td class="w-1/4 pb-3 pt-3 text-center">${file[1]}b</td>
                            <td class="w-1/4 pb-3 pt-3 text-center">
                            <button class="rounded-md p-2 text-xs bg-white" style="color: red" onclick="revealDecryptionPopUp('${file[0]}')">Decrypt</button>
                            </td>
                        </tr>`
    });
}