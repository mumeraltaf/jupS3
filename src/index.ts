import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import {
  MainAreaWidget
} from '@jupyterlab/apputils';

// import {
//   IFileBrowserFactory
// } from '@jupyterlab/filebrowser';

import {
  Widget
} from '@lumino/widgets';



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

    

    const content = new S3BrowserWidget();
        // @ts-ignore
    const widget = new MainAreaWidget({ content });
    widget.title.label = 'S3 Browser';
    app.shell.add(widget, 'left');

  }
};


class S3BrowserWidget extends Widget {
  constructor() {
    super();
    this.addClass('jp-S3BrowserWidget');
    this.id = 's3-browser-widget';
    this.title.label = 'S3 Browser';
    this.title.closable = true;

    this.node.innerHTML = `
      <div>
        <h2>S3 Bucket Contents</h2>
        <ul id="s3-contents"></ul>
      </div>
    `;

     requestAPI<any>('get-bucket-contents')
      .then(data => {
        const ul = this.node.querySelector('#s3-contents') as HTMLUListElement;
      data.data.forEach((item: string) => {
        const li = document.createElement('li');
        li.textContent = item;
        ul.appendChild(li);
      });
      })
      .catch(reason => {
        console.error(
          `Error getting S3 bucket contents.\n${reason}`
        );
      });

  }

}



export default plugin;
