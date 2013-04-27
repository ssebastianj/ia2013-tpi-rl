#ifndef GWOPCIONESDIALOG_H
#define GWOPCIONESDIALOG_H

#include <QDialog>

namespace Ui {
class GWOpcionesDialog;
}

class GWOpcionesDialog : public QDialog
{
    Q_OBJECT
    
public:
    explicit GWOpcionesDialog(QWidget *parent = 0);
    ~GWOpcionesDialog();
    
protected:
    void changeEvent(QEvent *e);
    
private:
    Ui::GWOpcionesDialog *ui;
};

#endif // GWOPCIONESDIALOG_H
