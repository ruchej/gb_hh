favoritesHandler = function favoritesHandler($icon, url) {
    const regex = /fav\/(\d+)\//;
    let objId = regex.exec(url)[1];
    let cntr = $icon.closest((`.obj-${objId}-card`));
    cntr.remove();
}
