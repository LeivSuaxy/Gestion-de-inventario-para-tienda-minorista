import { CommonModule } from '@angular/common';
import { AfterViewInit, Component, Renderer2, ElementRef } from '@angular/core';
import { Router, RouterLink, RouterLinkActive, NavigationEnd } from '@angular/router';

@Component({
  selector: 'app-tables',
  standalone: true,
  imports: [CommonModule, RouterLink, RouterLinkActive],
  templateUrl: './tables.component.html',
  styleUrl: './tables.component.css'
})
export class TablesComponent implements AfterViewInit{
  tablaActiva?: string;

  constructor(private router: Router, private renderer: Renderer2, private el: ElementRef) {
    this.router.events.subscribe(event => {
      if (event instanceof NavigationEnd) {
        this.updateActiveTable();
      }
    });
  }

  ngAfterViewInit() {
    this.updateActiveTable();
  }

  updateActiveTable() {
    // Asegúrate de que la lógica de ruta a tablaActiva esté actualizada
    if (this.router.url.includes('/product_table')) {
      this.tablaActiva = 'product';
    } else if (this.router.url.includes('/inventory_table')) {
      this.tablaActiva = 'inventory';
    } else if (this.router.url.includes('/employee_table')) {
      this.tablaActiva = 'employee';
    } else if (this.router.url.includes('/warehouse_table')) {
      this.tablaActiva = 'warehouse'
    } else if (this.router.url.includes('/messenger_table')){
      this.tablaActiva = 'messenger'
    } else if (this.router.url.includes('/purchase_order_table')){
      this.tablaActiva = 'purchase'
    }

    // Aplica el estilo
    this.applyStyles();
  }

  applyStyles() {
    const tables = this.el.nativeElement.querySelectorAll('.tables');
    tables.forEach((table: HTMLElement) => {
      this.renderer.removeStyle(table, 'background-color');
      if (table.querySelector(`a[routerLink="/tables/${this.tablaActiva}_table"]`)) {
        this.renderer.setStyle(table, 'background-color', '#282821');
      }
    });
  }
}
