import { bootstrapApplication } from '@angular/platform-browser';
import { appConfig } from './app/app.config';
import { AppComponent } from './app/app.component';

bootstrapApplication(AppComponent, appConfig)
  .catch((err) => console.error(err));

  window.addEventListener('load', adjustBackgroundHeight);
window.addEventListener('resize', adjustBackgroundHeight);

function adjustBackgroundHeight(): void {
  const html: HTMLElement = document.documentElement;

  // Usa scrollHeight de html para obtener la altura total del contenido del documento
  const height: number = html.scrollHeight;

  // Ajusta la altura mínima del body para que coincida con la altura total del contenido
  document.body.style.minHeight = `${height}px`;
}