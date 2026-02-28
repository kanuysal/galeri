const fs = require('fs');
let code = fs.readFileSync('assets/index-845b001d.js', 'utf-8');

// Replace static occurrences explicitly
code = code.replace(/>Signed</g, '>Sevgiyle yapıyoruz<');
code = code.replace(/Price\s+upon\s+request/g, 'Bilgi Alın');
code = code.replace(/Price\s+on\s+request/g, 'Bilgi Alın');
code = code.replace(/Available/g, 'İnegöl Mağaza');
code = code.replace(/Haute\s+Couture/g, 'Valencia Atellier');

// Let's refine the dynamic patch to handle the Contact button and 'Bilgi Alın' link
const newPatch = `
// --- MINA LIDYA DYNAMIC TRANSLATION PATCH V3 ---
setInterval(() => {
    // 1. Translate Keyboard Instructions & Generic Texts
    const textNodes = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
    let node;
    while (node = textNodes.nextNode()) {
        const val = node.nodeValue;
        if(val.includes('Scroll')) node.nodeValue = val.replace(/Scroll.*keys/gi, 'Kaydırma çubuğunu veya yön tuşlarını kullanın');
        if(val.includes('Signed')) node.nodeValue = val.replace('Signed', 'Sevgiyle yapıyoruz');
        if(val.includes('Available')) node.nodeValue = val.replace('Available', 'İnegöl Mağaza');
        if(val.includes('Haute Couture')) node.nodeValue = val.replace('Haute Couture', 'Valencia Atellier');
        if(val.includes('Unique Piece')) node.nodeValue = val.replace('Unique Piece', 'Aşkla giyiniz...');
        if(val.includes('Ink on paper')) node.nodeValue = val.replace('Ink on paper', 'Aşkla giyiniz...');
        if(val.includes('Contact me')) node.nodeValue = val.replace('Contact me', 'İletişim');
    }

    // 2. Fix Contact Button & Bilgi Alın link
    setTimeout(() => {
        // Fix Contact me button text explicitly
        const contactBtn = document.querySelector('.contact_button');
        if(contactBtn) {
            Array.from(contactBtn.childNodes).forEach(child => {
                if(child.nodeType === Node.TEXT_NODE && child.textContent.includes('Contact me')) {
                    child.textContent = child.textContent.replace('Contact me', 'İletişim');
                }
            });
            if(!contactBtn.hasAttribute('data-localized')) {
                const clone = contactBtn.cloneNode(true);
                contactBtn.replaceWith(clone);
                clone.setAttribute('data-localized', 'true');
                clone.style.pointerEvents = 'all';
                clone.addEventListener('click', (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    const titleElem = document.querySelector('h1.title');
                    const title = titleElem ? titleElem.innerText.trim() : 'Ürün';
                    window.open('https://wa.me/905421131641?text=' + encodeURIComponent(title + ' Hakkında Bilgi Almak İstiyorum'), '_blank');
                });
            }
        }

        // Fix Bilgi Alın specifically (it was raw text, need an A tag)
        document.querySelectorAll('span, p, div, li').forEach(el => {
            if(el.textContent.trim() === 'Bilgi Alın' && typeof el.innerHTML === 'string' && !el.innerHTML.includes('<a')) {
                const titleElem = document.querySelector('h1.title');
                const title = titleElem ? titleElem.innerText.trim() : 'Ürün';
                const waUrl = 'https://wa.me/905421131641?text=' + encodeURIComponent(title + ' Hakkında Bilgi Almak İstiyorum');
                el.innerHTML = '<a href="' + waUrl + '" target="_blank" style="color: inherit; text-decoration: underline; cursor: pointer; pointer-events: all; position: relative; z-index: 9999;">Bilgi Alın</a>';
            }
        });
    }, 100);

}, 500);
`;

// Extract anything before V1/V2/V3 patch and append cleanly
const patchIndex = code.indexOf('// --- MINA LIDYA DYNAMIC TRANSLATION PATCH');
if (patchIndex !== -1) {
    code = code.substring(0, patchIndex);
}
code += '\n' + newPatch;

fs.writeFileSync('assets/index-845b001d.js', code, 'utf-8');
console.log('Patch V3 applied successfully!');
