/* tslint:disable:no-unused-variable */
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { DebugElement } from '@angular/core';

import { Employee_tableComponent } from './employee_table.component';

describe('Employee_tableComponent', () => {
  let component: Employee_tableComponent;
  let fixture: ComponentFixture<Employee_tableComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ Employee_tableComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(Employee_tableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
