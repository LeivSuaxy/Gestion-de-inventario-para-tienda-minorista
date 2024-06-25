import { Component, OnInit, ViewChild } from '@angular/core';
import {SelectionModel} from '@angular/cdk/collections';
import {MatTableDataSource, MatTableModule} from '@angular/material/table';
import {MatCheckboxModule} from '@angular/material/checkbox';
import { TablesComponent } from '../tables.component';
import { StockComponent } from '../../../views/stock/stock.component';
import {HttpClient, HttpClientModule} from "@angular/common/http";
import {MatIconModule} from '@angular/material/icon';
import {MatButtonModule} from '@angular/material/button';
import { ButtonsComponent } from '../buttons/buttons.component';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatTable } from '@angular/material/table';
import { forkJoin, Observable } from 'rxjs';
import { CommonModule } from '@angular/common';

export interface Employee {
  carnet_identidad: string;
  nombre: string;
  salario: number;
  id_jefe: string;
}

@Component({
  selector: 'app-employee_table',
  templateUrl: './employee_table.component.html',
  styleUrls: ['./employee_table.component.css'],
  standalone: true,
  imports: [
    HttpClientModule,
    MatTableModule, 
    MatCheckboxModule, 
    TablesComponent, 
    StockComponent, 
    MatIconModule, 
    MatButtonModule,
    ButtonsComponent,
    MatFormFieldModule,
    MatInputModule,
    CommonModule
  ],
})
export class Employee_tableComponent implements OnInit {
  showConfirmDialog = false; // Controla la visibilidad del diálogo

  // Otros métodos y propiedades...
  openConfirmDialog() {
    this.showConfirmDialog = true;
  }

  deleteConfirmed() {
    this.showConfirmDialog = false;
    let filas: string[] = this.getSelectedRowsData();
    filas.forEach((element) => {
      this.eliminarElemento(element);
    });
    this.deleteEmployees();
  }

  @ViewChild(MatTable) table!: MatTable<any>;

  eliminarElemento(id: string) {
    // Eliminar el elemento de la fuente de datos
    const index = this.dataSource.data.findIndex(item => item.carnet_identidad === id);
    if (index > -1) {
      this.dataSource.data.splice(index, 1);
      // Actualizar el dataSource
      this.dataSource.data = [...this.dataSource.data];
      // Refrescar la tabla, si es necesario
      // this.table.renderRows();
    }
  }

  // Datos para configurar la tabla
  data: any;
  employees: Employee[] = []
  dataSource: MatTableDataSource<Employee> = new MatTableDataSource<Employee>(this.employees);
  displayedColumns: string[] = ['select', 'carnet_identidad', 'nombre', 'salario', 'id_jefe'];
  selection = new SelectionModel<Employee>(true, []);
  apiUrl: string = 'http://localhost:8000/api/admin/employees/'

  constructor(private http: HttpClient) { 
    
  }

  // Llamada a la API para extraer los datos y guardarlos en dataSource
  async ngOnInit() {
    await this.apicall();
    this.dataSource = new MatTableDataSource<Employee>(this.employees);
  }

  // Extracción de datos de la API
  private async apicall(): Promise<void> {
    if (this.apiUrl) {
      try {
        const response = await this.http.get(this.apiUrl).toPromise();
        this.data = response;
        this.traslate();
      } catch (error) {
        console.error(error);
      }
    }
  }
  
  // Traducción de los datos obtenidos de la API
  traslate(): void {
    this.employees.push(...this.data['elements'].map((element: any) => ({
      carnet_identidad: element.carnet_identidad,
      nombre: element.nombre,
      salario: element.salario,
      id_jefe: element.id_jefe ? element.id_jefe : "-"
    })));
  }

  // Busqueda de datos en la tabla
  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();
  }

  // Devuelve si estan todas las filas seleccionadas
  isAllSelected() {
    console.log(this.getSelectedRowsData());
    const numSelected = this.selection.selected.length;
    const numRows = this.dataSource.data.length;
    return numSelected === numRows;
  }

  // Selecciona todas las filas, si ya todas estan seleccionadas las deselecciona
  toggleAllRows() {
    if (this.isAllSelected()) {
      this.selection.clear();
      return;
    }

    this.selection.select(...this.dataSource.data);
  }

  // Devuelve en un arreglo todas las filas seleccionadas
  getSelectedRowsData(): string[] {
    let ids: any[] = [];

    this.selection.selected.forEach((element) => {
      ids.push(element.carnet_identidad);
    });
  
    return ids;
  }

  eliminarEmpleados(carnetIds: string[]) {
    const observables = carnetIds.map(id => 
      this.http.post('http://localhost:8000/api/admin/delete_inventory/', { ci: id }),
    );
    return forkJoin(observables);
  }

  deleteEmployees() {
    this.eliminarEmpleados(this.getSelectedRowsData()).subscribe({
      next: (response) => console.log('Empleados eliminados', response),
      error: (error) => console.error('Error al eliminar empleados', error)
    });
  }

  // Muestra en consola las filas seleccionadas
  showSelectedRowsData(): void {
    const selectedRows = this.getSelectedRowsData();
    console.log('Filas seleccionadas:', selectedRows);
  }

  // Selecciona una casilla
  checkboxLabel(row?: Employee): string {
    if (!row) {
      return `${this.isAllSelected() ? 'deselect' : 'select'} all`;
    }
    return `${this.selection.isSelected(row) ? 'deselect' : 'select'} row ${row.carnet_identidad + 1}`;
  }

}
