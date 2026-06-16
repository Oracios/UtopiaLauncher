const { DistributionAPI } = require('helios-core/common')

const ConfigManager = require('./configmanager')

// Hébergé sur le serveur Nerysia (sous-dossier Utopia).
exports.REMOTE_DISTRO_URL = 'https://apk.nerysia.fr/utopia-laucher/distribution.json'

const api = new DistributionAPI(
    ConfigManager.getLauncherDirectory(),
    null, // Injected forcefully by the preloader.
    null, // Injected forcefully by the preloader.
    exports.REMOTE_DISTRO_URL,
    false
)

exports.DistroAPI = api