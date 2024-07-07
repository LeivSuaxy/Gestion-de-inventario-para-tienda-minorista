import { CommonModule } from '@angular/common';
import { AfterViewInit, Component, Renderer2, ElementRef } from '@angular/core';
import { Router, RouterLink, RouterLinkActive, NavigationEnd } from '@angular/router';

interface TableMap {
  [key: string]: string;
}

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
    const tableMap: TableMap = {
      '/product_table': 'product',
      '/inventory_table': 'inventory',
      '/employee_table': 'employee',
      '/warehouse_table': 'warehouse',
      '/messenger_table': 'messenger',
      '/purchase_order_table': 'purchase_order'
    };
  
    // Encuentra la primera coincidencia en el mapa
    const foundKey = Object.keys(tableMap).find(key => this.router.url.includes(key));
    if (foundKey) {
      console.log(tableMap[foundKey]);
      this.tablaActiva = tableMap[foundKey];
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
