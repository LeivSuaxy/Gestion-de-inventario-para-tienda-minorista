import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PostcarComponent } from './postcar.component';

describe('PostcarComponent', () => {
  let component: PostcarComponent;
  let fixture: ComponentFixture<PostcarComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PostcarComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(PostcarComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
