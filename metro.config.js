const { getDefaultConfig } = require('expo/metro-config');

const config = getDefaultConfig(__dirname);

// Configuración para evitar problemas de cache
config.resetCache = true;

// Configuración del resolver para evitar cache
config.resolver = {
  ...config.resolver,
  // Evitar cache de resolución de módulos
  enableGlobalPackages: false,
};

// Configuración del transformer
config.transformer = {
  ...config.transformer,
  // Evitar cache del transformer
  enableBabelRCLookup: false,
  enableBabelRuntime: false,
};

// Configuración del cache
config.cacheStores = [];

module.exports = config; 