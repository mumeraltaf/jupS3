import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { ISettingRegistry } from '@jupyterlab/settingregistry';

import { requestAPI } from './handler';

/**
 * Initialization data for the jupS3 extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'jupS3:plugin',
  description: 'A JupyterLab extension.',
  autoStart: true,
  optional: [ISettingRegistry],
  activate: (app: JupyterFrontEnd, settingRegistry: ISettingRegistry | null) => {
    console.log('JupyterLab extension jupS3 is activated!');

    if (settingRegistry) {
      settingRegistry
        .load(plugin.id)
        .then(settings => {
          console.log('jupS3 settings loaded:', settings.composite);
        })
        .catch(reason => {
          console.error('Failed to load settings for jupS3.', reason);
        });
    }

    requestAPI<any>('get-example')
      .then(data => {
        console.log(data);
      })
      .catch(reason => {
        console.error(
          `The jupS3 server extension appears to be missing.\n${reason}`
        );
      });

    requestAPI<any>('get-bucket-contents')
      .then(data => {
        console.log(data);
      })
      .catch(reason => {
        console.error(
          `Error getting S3 bucket contents.\n${reason}`
        );
      });

  }
};

export default plugin;
