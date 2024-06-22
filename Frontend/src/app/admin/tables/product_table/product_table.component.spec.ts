/* tslint:disable:no-unused-variable */
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { DebugElement } from '@angular/core';

import { Product_tableComponent } from './product_table.component';

describe('Product_tableComponent', () => {
  let component: Product_tableComponent;
  let fixture: ComponentFixture<Product_tableComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ Product_tableComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(Product_tableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
