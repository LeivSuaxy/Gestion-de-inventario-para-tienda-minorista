/* tslint:disable:no-unused-variable */
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { DebugElement } from '@angular/core';

import { Inventory_tableComponent } from './inventory_table.component';

describe('Inventory_tableComponent', () => {
  let component: Inventory_tableComponent;
  let fixture: ComponentFixture<Inventory_tableComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ Inventory_tableComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(Inventory_tableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
