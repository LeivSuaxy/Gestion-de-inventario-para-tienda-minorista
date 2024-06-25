/* tslint:disable:no-unused-variable */
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { DebugElement } from '@angular/core';

import { Post_inventoryComponent } from './post_inventory.component';

describe('Post_inventoryComponent', () => {
  let component: Post_inventoryComponent;
  let fixture: ComponentFixture<Post_inventoryComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ Post_inventoryComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(Post_inventoryComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
