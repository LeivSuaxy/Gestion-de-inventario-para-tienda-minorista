/* tslint:disable:no-unused-variable */
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { DebugElement } from '@angular/core';

import { Post_warehouseComponent } from './post_warehouse.component';

describe('Post_warehouseComponent', () => {
  let component: Post_warehouseComponent;
  let fixture: ComponentFixture<Post_warehouseComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ Post_warehouseComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(Post_warehouseComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
