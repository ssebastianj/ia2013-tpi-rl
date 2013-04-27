#ifndef GWGENRNDESTADOSDIALOG_H
#define GWGENRNDESTADOSDIALOG_H

#include <QDialog>

namespace Ui {
class GWGenRndEstadosDialog;
}

class GWGenRndEstadosDialog : public QDialog
{
    Q_OBJECT
    
public:
    explicit GWGenRndEstadosDialog(QWidget *parent = 0);
    ~GWGenRndEstadosDialog();
    
protected:
    void changeEvent(QEvent *e);
    
private:
    Ui::GWGenRndEstadosDialog *ui;
};

#endif // GWGENRNDESTADOSDIALOG_H
