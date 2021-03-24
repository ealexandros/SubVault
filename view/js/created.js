(async function getVaultFiles() {
    const vaultFiles = await eel.sub_vault_search()();
    if(vaultFiles == null) return;

    const table = document.getElementById('vault_table');
    table.innerHTML = `<thead>
                        <tr class="text-2xl" style="border-bottom: 3px solid red;">
                        <td class="w-1/2 pb-1 pt-1 text-left">Already Found</td>
                        <td class="w-1/4 pb-1 pt-1 text-center">Size</td>
                        <td class="w-1/4 pb-1 pt-1 text-center">Pick</td>
                        </tr>
                    </thead>`;
    vaultFiles.forEach(file => {
        table.innerHTML += `<tr style="border-bottom: 3px solid red;">
                            <td class="w-1/2 pb-3 pt-3 font-bold">${file[0]}</td>
                            <td class="w-1/4 pb-3 pt-3 text-center">${file[1]}b</td>
                            <td class="w-1/4 pb-3 pt-3 text-center">
                            <button class="rounded-md p-2 text-xs bg-white" style="color: red" onclick="revealDecryptionPopUp('${file[0]}')">Decrypt</button>
                            </td>
                        </tr>`
    });
})();