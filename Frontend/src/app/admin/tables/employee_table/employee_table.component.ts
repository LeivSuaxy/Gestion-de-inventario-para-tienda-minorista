import { Component, OnInit, AfterViewInit, ViewChild } from '@angular/core';
import {MatPaginator, MatPaginatorModule} from '@angular/material/paginator';
import {MatSort, MatSortModule} from '@angular/material/sort';
import {MatTableDataSource, MatTableModule} from '@angular/material/table';
import {MatInputModule} from '@angular/material/input';
import {MatFormFieldModule} from '@angular/material/form-field';
import { Venta } from '../../../views/stock/cartservice.service';
import { TablesComponent } from '../tables.component';
import {SelectionModel} from '@angular/cdk/collections';
import {MatCheckboxModule} from '@angular/material/checkbox';

export interface Employee {
  carnetID: string;
  nombre: string;
  salario: number;
  id_jefe: string;
}

@Component({
  selector: 'app-employee_table',
  templateUrl: './employee_table.component.html',
  styleUrls: ['./employee_table.component.css'],
  standalone: true,
  imports: [MatTableModule, MatCheckboxModule, TablesComponent],
})
export class Employee_tableComponent implements OnInit {

  displayedColumns: string[] = ['select', 'carnetID', 'nombre', 'salario', 'id_jefe'];
  dataSource = new MatTableDataSource<Employee>();
  selection = new SelectionModel<Employee>(true, []);

  isAllSelected() {
    const numSelected = this.selection.selected.length;
    const numRows = this.dataSource.data.length;
    return numSelected === numRows;
  }

  toggleAllRows() {
    if (this.isAllSelected()) {
      this.selection.clear();
      return;
    }

    this.selection.select(...this.dataSource.data);
  }

  /** The label for the checkbox on the passed row */
  checkboxLabel(row?: Employee): string {
    if (!row) {
      return `${this.isAllSelected() ? 'deselect' : 'select'} all`;
    }
    return `${this.selection.isSelected(row) ? 'deselect' : 'select'} row ${row.carnetID + 1}`;
  }

  constructor() { }

  ngOnInit() {

  }

}
