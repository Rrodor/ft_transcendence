window.onload = function() {
    var regex = /(\w+)_changed=true/;
    var match = window.location.search.match(regex);
    if (match) {
        var newUrl = window.location.href.split('?')[0];
        window.history.replaceState({}, '', newUrl);

        // Ajouter un gestionnaire d'événements click au bouton de fermeture du message
        var closeButton = document.querySelector('.btn-close');
        if (closeButton) {
            closeButton.addEventListener('click', function() {
                window.location.reload(true);
            });
        }
    }
};