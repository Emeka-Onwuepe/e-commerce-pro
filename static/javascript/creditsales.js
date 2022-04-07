const amounts = document.getElementsByClassName('amount')

for (const node of amounts) {
    node.innerHTML = addComas(node.innerHTML.replace(/,/g, ''))
}