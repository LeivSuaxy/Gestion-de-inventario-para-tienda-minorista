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
  MatDialogContent,
  MatDialogModule,
  MatDialogRef,
  MatDialogTitle,
} from '@angular/material/dialog';

export interface Inventario {
  id: string;
  categoria: string;
  id_almacen: string;
}

@Component({
  selector: 'app-inventory_table',
  templateUrl: './inventory_table.component.html',
  styleUrls: ['./inventory_table.component.css'],
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
export class Inventory_tableComponent implements OnInit {
  readonly dialog = inject(MatDialog);

  // Configuracion del cuadro de dialogo
  openDialog(enterAnimationDuration: string, exitAnimationDuration: string): void {
    const dialogRef = this.dialog.open(DeleteDialog, {
      width: '250px',
      enterAnimationDuration,
      exitAnimationDuration,
      position: { top: '-35%', left: '40%' },
      hasBackdrop: true,
      disableClose: true,
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
  inventarios: Inventario[] = []

  dataSource: MatTableDataSource<Inventario> = new MatTableDataSource<Inventario>(this.inventarios);
  displayedColumns: string[] = ['select', 'id_producto', 'nombre', 'categoria', 'stock', 'precio'];
  selection = new SelectionModel<Inventario>(true, []);
  apiUrl: string = 'http://localhost:8000/api/admin/objects/'

  constructor(private http: HttpClient) { 
    
  }

  async ngOnInit() {
    //await this.apicall();
    this.dataSource = new MatTableDataSource<Inventario>(this.inventarios);
  }

  /*private async apicall(): Promise<void> {
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
    this.products.push(...this.data['elements'].map((element: any) => ({
      nombre: element.nombre,
      id_producto: element.id_producto,
      precio: element.precio,
      stock: element.stock,
      categoria: element.categoria,
      descripcion: element.descripcion,
      imagen: element.imagen,
    })));
  }*/

  getSelectedRowsData(): string[] {
    let ids: any[] = [];

    this.selection.selected.forEach((element) => {
      ids.push(element.id);
    });
  
    return ids;
  }

  eliminarInventario(ids: string[]) {
    return this.http.delete('http://localhost:8000/api/admin/delete_inventory/', { body: { ci: ids } });
  }

  deleteInventory() {
    this.eliminarInventario(this.getSelectedRowsData()).subscribe({
      next: (response) => console.log('Inventarios eliminados', response),
      error: (error) => console.error('Error al eliminar inventarios', error)
    });
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

  /** The label for the checkbox on the passed row */
  checkboxLabel(row?: Inventario): string {
    if (!row) {
      return `${this.isAllSelected() ? 'deselect' : 'select'} all`;
    }
    return `${this.selection.isSelected(row) ? 'deselect' : 'select'} row ${row.id + 1}`;
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
