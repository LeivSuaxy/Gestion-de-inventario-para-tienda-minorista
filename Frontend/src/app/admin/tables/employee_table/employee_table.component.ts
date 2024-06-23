import { Component, OnInit, inject, ChangeDetectionStrategy } from '@angular/core';
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
import {
  MatDialog,
  MatDialogActions,
  MatDialogClose,
  MatDialogConfig,
  MatDialogContent,
  MatDialogModule,
  MatDialogRef,
  MatDialogTitle,
} from '@angular/material/dialog';
import { MAT_SELECT_SCROLL_STRATEGY } from '@angular/material/select';

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
    MatInputModule
  ],
})
export class Employee_tableComponent implements OnInit {
  readonly dialog = inject(MatDialog);

  openDialog(enterAnimationDuration: string, exitAnimationDuration: string): void {
    const dialogRef = this.dialog.open(DeleteDialog, {
      width: '250px',
      enterAnimationDuration,
      exitAnimationDuration,
      position: { top: '-35%', left: '40%' },
      hasBackdrop: true,
      disableClose: true,
      backdropClass: 'custom-backdrop-class',
    });
  
    document.body.style.overflow = 'hidden'; // Deshabilita el desplazamiento
  
    // Función para detener la propagación de eventos de clic fuera del diálogo
    const stopClickPropagation = (e: MouseEvent) => {
      const overlayContainer = document.querySelector('.cdk-overlay-container');
      if (overlayContainer && !overlayContainer.contains(e.target as Node)) {
        e.stopPropagation();
        e.preventDefault();
      }
    };
  
    // Agrega el manejador de eventos al documento
    document.addEventListener('click', stopClickPropagation, true);
  
    dialogRef.afterClosed().subscribe(() => {
      document.body.style.overflow = ''; // Re-habilita el desplazamiento
      // Importante: remover el manejador de eventos una vez que el diálogo se cierra
      document.removeEventListener('click', stopClickPropagation, true);
    });
  }

  data: any;
  employees: Employee[] = []

  dataSource: MatTableDataSource<Employee> = new MatTableDataSource<Employee>(this.employees);
  displayedColumns: string[] = ['select', 'carnet_identidad', 'nombre', 'salario', 'id_jefe'];
  selection = new SelectionModel<Employee>(true, []);
  apiUrl: string = 'http://localhost:8000/api/admin/employees/'

  constructor(private http: HttpClient) { 
    
  }

  async ngOnInit() {
    await this.apicall();
    this.dataSource = new MatTableDataSource<Employee>(this.employees);
  }

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
  
  traslate(): void {
    this.employees.push(...this.data['elements'].map((element: any) => ({
      carnet_identidad: element.carnet_identidad,
      nombre: element.nombre,
      salario: element.salario,
      id_jefe: element.id_jefe ? element.id_jefe : "-"
    })));
  }

  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();
  }

  /** Whether the number of selected elements matches the total number of rows. */
  isAllSelected() {
    const numSelected = this.selection.selected.length;
    const numRows = this.dataSource.data.length;
    return numSelected === numRows;
  }

  /** Selects all rows if they are not all selected; otherwise clear selection. */
  toggleAllRows() {
    if (this.isAllSelected()) {
      this.selection.clear();
      return;
    }

    this.selection.select(...this.dataSource.data);
  }

  getSelectedRowsData(): Employee[] {
    return this.selection.selected;
  }

  showSelectedRowsData(): void {
    const selectedRows = this.getSelectedRowsData();
    console.log('Filas seleccionadas:', selectedRows);
  }

  /** The label for the checkbox on the passed row */
  checkboxLabel(row?: Employee): string {
    if (!row) {
      return `${this.isAllSelected() ? 'deselect' : 'select'} all`;
    }
    return `${this.selection.isSelected(row) ? 'deselect' : 'select'} row ${row.carnet_identidad + 1}`;
  }

}

@Component({
  selector: 'delete-dialog',
  templateUrl: 'delete-dialog.html',
  standalone: true,
  imports: [MatButtonModule, MatDialogActions, MatDialogClose, MatDialogTitle, MatDialogContent, MatDialogModule],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class DeleteDialog {
  readonly dialogRef = inject(MatDialogRef<DeleteDialog>);
}
