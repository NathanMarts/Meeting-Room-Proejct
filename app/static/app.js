function data() {
  return {
    newReserveModal: {
      show: false,
      open() { this.show = true },
      close() { this.show = false },
      isOpen() { return this.show },
    },
    reserveModal: {
      show: false,
      open() { this.show = true },
      close() { this.show = false },
      isOpen() { return this.show },
    },
    toastService: {
      toasts: [],
      error(message) {
        const toast = {
          type: 'error',
          message: message,
          visible: false,
        }
        this.toasts.push(toast);
        setTimeout(() => {
          this.toasts[this.toasts.length - 1].visible = true;
        }, 10);
        setTimeout(() => {
          this.removeToast(0)
        }, 3000);
      },
      success(message) {
        const toast = {
          type: 'success',
          message: message,
          visible: false,
        }
        this.toasts.push(toast);
        setTimeout(() => {
          this.toasts[this.toasts.length - 1].visible = true;
        }, 10);
        setTimeout(() => {
          this.removeToast(0)
        }, 3010);
      },
      removeToast(index) {
        if (this.toasts.length > 0) {
          this.toasts[index].visible = false;
          setTimeout(() => {
            this.toasts.shift()
          }, 300);
        }
      }
    }
  }
}