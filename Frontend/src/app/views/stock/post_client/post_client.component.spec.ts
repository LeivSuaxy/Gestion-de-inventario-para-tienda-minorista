/* tslint:disable:no-unused-variable */
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { DebugElement } from '@angular/core';

import { Post_clientComponent } from './post_client.component';

describe('Post_clientComponent', () => {
  let component: Post_clientComponent;
  let fixture: ComponentFixture<Post_clientComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ Post_clientComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(Post_clientComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
