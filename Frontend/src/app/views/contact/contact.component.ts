import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { StyleManagerService } from '../../styleManager.service';

@Component({
  selector: 'app-contact',
  templateUrl: './contact.component.html',
  styleUrls: ['./contact.component.css'],
  standalone: true,
  imports: [CommonModule, FormsModule]
})
export class ContactComponent {
  name? : string;
  email? : string;
  content? : string;

  constructor(private http : HttpClient, private styleManager: StyleManagerService) {}

  showConfirmDialog = false; // Controla la visibilidad del diálogo

  // Otros métodos y propiedades...
  openConfirmDialog() {
    this.showConfirmDialog = true;
    const body = document.getElementById("contact");

    if (body instanceof HTMLElement){
        body.classList.add('blur-background');
    }
    this.styleManager.setBlurBackground(true);
  }

  closeConfirmDialog() {
    this.showConfirmDialog = false;
    const body = document.getElementById("contact");

    if (body instanceof HTMLElement){
        body.classList.remove('blur-background');
    }
    this.styleManager.setBlurBackground(false);
  }

  async posMethod(): Promise<void> {
    let url = 'http://localhost:8000/api/correo/contact/';
    const contentData = {
        name: this.name ? this.name : '',
        email: this.email ? this.email : '',
        content: this.content ? this.content : '',
    };
  
    try {
      this.showConfirmDialog = false;
      this.name = this.email = this.content = undefined;
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(contentData)
      });
  
      if (!response.ok) {
        throw new Error('Network response was not ok');
        this.notification('error');
      } else {
        console.log('Network response was ok');
        this.notification('success');
      }
  
      const data = await response.json();
      console.log(data);
      

    } catch (error) {
      console.error('There was a problem with your fetch operation:', error);
    }
  }

  cancel(): void {
    
  }

  notification(type: 'error' | 'success'): void {
    const notification = document.getElementById('notification');
    if (notification instanceof HTMLElement) {
      notification.classList.add('notification-transition'); // Asegura que la transición esté aplicada
      notification.style.position = 'fixed';
      notification.style.right = '2vh';
      notification.style.bottom = '14.2vh';
      notification.style.display = 'block';
      notification.style.opacity = '0'; // Inicia invisible para la animación
  
      // Establece el color de fondo y el texto basado en el tipo de notificación
      if (type === 'error') {
        notification.style.backgroundColor = 'red';
        notification.textContent = 'Error sending message';
      } else if (type === 'success') {
        notification.style.backgroundColor = 'chartreuse';
        notification.textContent = 'Message sent successfully';
      }
  
      // Inicia visible para la animación
      setTimeout(() => {
        notification.style.opacity = '0.7';
      }, 10); // Un pequeño retraso asegura que el navegador aplique la transición
  
      // Inicia la desaparición después de 2 segundos
      setTimeout(() => {
        notification.style.opacity = '0';
        // Oculta completamente después de que la transición de opacidad termine
        setTimeout(() => {
          notification.style.display = 'none';
        }, 500); // Coincide con la duración de la transición de opacidad
      }, 2000);
    }
  }

}
