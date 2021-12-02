import { Config } from "./types";
import { uiConfig } from "./uiConfig";
import { Feature, FeatureItem } from "hooks/services/Feature";

const Features: Feature[] = [
  {
    id: FeatureItem.AllowUploadCustomImage,
  },
  {
    id: FeatureItem.AllowCustomDBT,
  },
  {
    id: FeatureItem.AllowUpdateConnectors,
  },
];

const defaultConfig: Config = {
  ui: uiConfig,
  segment: { enabled: true, token: "" },
  healthCheckInterval: 10000,
  version: "dev",
  apiUrl: `${window.location.protocol}//${window.location.hostname}:8001/api/v1/`,
  integrationUrl: "/docs",
  oauthRedirectUrl: `${window.location.protocol}//${window.location.host}`,
  isDemo: false,
  features: Features,
};

export { defaultConfig };
