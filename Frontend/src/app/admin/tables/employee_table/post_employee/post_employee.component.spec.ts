/* tslint:disable:no-unused-variable */
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { DebugElement } from '@angular/core';

import { Post_employeeComponent } from './post_employee.component';

describe('Post_employeeComponent', () => {
  let component: Post_employeeComponent;
  let fixture: ComponentFixture<Post_employeeComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ Post_employeeComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(Post_employeeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
